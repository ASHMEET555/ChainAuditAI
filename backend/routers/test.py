from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import pandas as pd
from datetime import datetime
from core.database import SessionLocal
from models.fraud_log import FraudLog
from services.ai_service import detect_fraud, initialize_service
from services.chain_service import log_fraud_to_chain

router = APIRouter(prefix="/test", tags=["Testing & Fraud Detection"])

# Initialize service on startup
initialize_service()


# ============= Input Schema =============

class FraudDetectionRequest(BaseModel):
    """
    Request for fraud detection.
    
    Each request is for ONE transaction type only.
    The form specifies which type of fraud detection to run.
    """
    transaction_type: str  # "vehicle", "bank", "ecommerce", or "ethereum"
    transaction_data: Dict  # Raw transaction features
    tx_hash: Optional[str] = None  # Optional transaction identifier


# ============= Output Schema =============

class FraudDetectionResult(BaseModel):
    """Response from fraud detection."""
    success: bool
    fraud_score: int  # 0-100
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    probability: float
    raw_prediction: int  # 0 or 1
    transaction_type: str
    database_id: Optional[int] = None
    blockchain_tx: Optional[str] = None


# ============= Endpoints =============

@router.post("/detect", response_model=FraudDetectionResult)
def detect_transaction_fraud(request: FraudDetectionRequest):
    """
    Detect fraud for a single transaction.
    
    Pipeline:
    1. Validate transaction_type (vehicle, bank, ecommerce, ethereum)
    2. Load appropriate model and transform function
    3. Transform raw transaction_data
    4. Run inference → binary output (0 or 1)
    5. Convert to probability (0.25 or 0.75)
    6. Convert to fraud_score (0-100)
    7. Store in database with transaction_type, fraud_score, risk_level
    8. If fraud_score > threshold, log to blockchain
    9. Return fraud detection result
    
    Args:
        request: TransactionType, transaction data, optional tx_hash
    
    Returns:
        Fraud detection result with score, risk level, and database ID
    
    Raises:
        HTTPException: If transaction_type is invalid or processing fails
    """
    valid_types = ["vehicle", "bank", "ecommerce", "ethereum"]
    
    if request.transaction_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transaction_type. Must be one of: {', '.join(valid_types)}"
        )
    
    try:
        # Step 1-6: Run fraud detection
        result = detect_fraud(request.transaction_data, request.transaction_type)
        
        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=f"Fraud detection failed: {result.get('error', 'Unknown error')}"
            )
        
        # Step 7: Store in database
        db = SessionLocal()
        fraud_log = FraudLog(
            tx_hash=request.tx_hash or f"local_{datetime.now().timestamp()}",
            transaction_type=request.transaction_type,
            fraud_score=result["fraud_score"],
            risk_level=result["risk_level"],
            probability=result["probability"],
            raw_prediction=result["raw_prediction"],
            model_version="v1",
            transaction_data=request.transaction_data
        )
        db.add(fraud_log)
        db.commit()
        db.refresh(fraud_log)
        
        blockchain_tx = None
        
        # Step 8: Log to blockchain if fraud_score > threshold
        FRAUD_THRESHOLD = 50  # Log to blockchain if score > 50
        if result["fraud_score"] > FRAUD_THRESHOLD:
            try:
                # Create feature vector for blockchain logging
                features_list = [
                    request.transaction_data.get(f"feature_{i}", 0.0)
                    for i in range(10)
                ]
                
                blockchain_tx = log_fraud_to_chain(
                    features_list,
                    result["fraud_score"]
                )
                
                # Update database with blockchain info
                fraud_log.blockchain_tx_hash = blockchain_tx
                db.commit()
            
            except Exception as chain_error:
                # Log warning but don't fail the request
                print(f"Warning: Could not log to blockchain: {chain_error}")
        
        db.close()
        
        # Step 9: Return result
        return FraudDetectionResult(
            success=True,
            fraud_score=result["fraud_score"],
            risk_level=result["risk_level"],
            probability=result["probability"],
            raw_prediction=result["raw_prediction"],
            transaction_type=request.transaction_type,
            database_id=fraud_log.id,
            blockchain_tx=blockchain_tx
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test-connection")
def test_connection():
    """
    Health check endpoint to verify service is running.
    
    Returns:
        Status message with supported transaction types
    """
    return {
        "status": "ok",
        "service": "FraudProof Ledger - Fraud Detection Engine",
        "timestamp": datetime.now().isoformat(),
        "supported_types": ["vehicle", "bank", "ecommerce", "ethereum"],
        "fraud_threshold": 50
    }

