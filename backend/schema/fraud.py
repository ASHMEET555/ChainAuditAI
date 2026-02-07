from pydantic import BaseModel
from typing import List, Dict, Optional


# ============= Input Schemas =============

class TransactionInput(BaseModel):
    """Input for single transaction fraud detection."""
    transaction_data: Dict
    transaction_type: Optional[str] = "general"
    tx_hash: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "transaction_data": {
                    "amount": 100.50,
                    "merchant_category": "5411",
                    "is_online": True,
                    "days_since_last_transaction": 5
                },
                "transaction_type": "ecommerce",
                "tx_hash": "0x123abc..."
            }
        }


class BulkTestInput(BaseModel):
    """Input for bulk transaction testing."""
    records: List[List[float]]


class ManualTestInput(BaseModel):
    """Input for manual feature-based testing."""
    features: List[float]


class HTMLFormInput(BaseModel):
    """Input schema for HTML form submissions."""
    # Vehicle Insurance Fields (optional)
    months_as_customer: Optional[int] = None
    age: Optional[int] = None
    policy_annual_premium: Optional[float] = None
    number_of_vehicles: Optional[int] = None
    
    # Bank Account Fields (optional)
    account_age_days: Optional[int] = None
    transaction_amount: Optional[float] = None
    transaction_frequency: Optional[int] = None
    average_daily_balance: Optional[float] = None
    
    # E-commerce Fields (optional)
    purchase_amount: Optional[float] = None
    device_type: Optional[str] = None
    shipping_address_matches_billing: Optional[bool] = None
    customer_age: Optional[int] = None
    
    # Ethereum/Blockchain Fields (optional)
    transaction_value_eth: Optional[float] = None
    gas_price: Optional[float] = None
    contract_interaction: Optional[bool] = None
    sender_transaction_count: Optional[int] = None
    
    # Common Fields
    transaction_type: Optional[str] = "general"
    tx_hash: Optional[str] = None


# ============= Output Schemas =============

class ModelScoreDetail(BaseModel):
    """Detail of individual model score."""
    model: str
    raw_prediction: int
    probability: float
    fraud_score: int


class FraudDetectionResponse(BaseModel):
    """Response from fraud detection endpoint."""
    success: bool
    fraud_score: int
    risk_level: str
    transaction_type: str
    model_details: List[Dict]
    database_id: Optional[int] = None


class BulkDetectionResponse(BaseModel):
    """Response from bulk fraud detection."""
    success: bool
    total_transactions: int
    results: List[Dict]


class TxIndex(BaseModel):
    """Transaction record index."""
    tx_hash: str
    transaction_type: str
    model_version: str

