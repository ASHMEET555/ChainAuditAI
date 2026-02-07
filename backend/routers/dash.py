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


@router.get("/{record_id}")
def get_fraud_record(record_id: int):
    """
    Get single fraud detection record by ID.
    
    Args:
        record_id: Database record ID
    
    Returns:
        Single fraud detection record with details
    """
    db = SessionLocal()
    record = db.query(FraudLog).filter(FraudLog.id == record_id).first()
    db.close()
    
    if not record:
        return {"error": "Record not found"}
    
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
        "transaction_data": record.transaction_data,
        "blockchain_tx_hash": record.blockchain_tx_hash
    }
    
    # If logged to blockchain, fetch on-chain data
    if record.blockchain_tx_hash:
        try:
            chain_data = get_onchain_fraud_data(record.blockchain_tx_hash)
            item["blockchain_data"] = chain_data
        except Exception as e:
            item["blockchain_data"] = {"error": str(e)}
    
    return item


@router.get("/type/{transaction_type}")
def get_records_by_type(transaction_type: str):
    """
    Get all fraud detection records for a specific transaction type.
    
    Args:
        transaction_type: One of "vehicle", "bank", "ecommerce", "ethereum"
    
    Returns:
        List of records for the specified type
    """
    db = SessionLocal()
    records = db.query(FraudLog).filter(
        FraudLog.transaction_type == transaction_type
    ).order_by(FraudLog.created_at.desc()).all()
    db.close()
    
    response = []
    for record in records:
        item = {
            "id": record.id,
            "tx_hash": record.tx_hash,
            "fraud_score": record.fraud_score,
            "risk_level": record.risk_level,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "blockchain_tx_hash": record.blockchain_tx_hash
        }
        response.append(item)
    
    return {
        "transaction_type": transaction_type,
        "total_records": len(response),
        "records": response
    }

