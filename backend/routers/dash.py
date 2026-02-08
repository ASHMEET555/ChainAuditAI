from fastapi import APIRouter
from core.database import SessionLocal
from models.fraud_log import FraudLog
from services.chain_service import get_onchain_fraud_data

router = APIRouter(prefix="/dash", tags=["Dashboard"])


@router.get("/")
def dashboard_stream():
    """
    Get all fraud detection logs from database.
    
    Returns fraud logs stored from test endpoint runs.
    For each log with blockchain transaction, fetch on-chain data.
    
    Returns:
        List of fraud detection records with optional on-chain data
    """
    db = SessionLocal()
    records = db.query(FraudLog).order_by(FraudLog.created_at.desc()).all()
    db.close()

    response = []
    for record in records:
        item = {
            "id": record.id,
            "tx_hash": record.tx_hash,
            "transaction_type": record.transaction_type,
            "fraud_score": record.fraud_score,
            "risk_level": record.risk_level,
            "probability": record.probability,
            "raw_prediction": record.raw_prediction,
            "model_version": record.model_version,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "blockchain_tx_hash": record.blockchain_tx_hash
        }
        
        # If logged to blockchain, fetch on-chain data
        if record.blockchain_tx_hash:
            try:
                chain_data = get_onchain_fraud_data(record.blockchain_tx_hash)
                item["blockchain_data"] = chain_data
            except Exception as e:
                item["blockchain_data"] = {"error": str(e)}
        
        response.append(item)
    
    return {
        "total_records": len(response),
        "records": response
    }

