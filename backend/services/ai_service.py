import joblib
import numpy as np
import pandas as pd
from typing import Dict, Tuple
from load_models import (
    load_model_vehicle,
    load_model_bank,
    load_model_ecommerce,
    load_model_eth
)
from transforms import (
    transform_vehicle_fraud_data,
    transform_bank_fraud_data,
    transform_ecommerce_fraud_data,
    transform_eth_fraud_data
)


class FraudDetectionService:
    """
    Single-model fraud detection service.
    
    Each transaction type uses its dedicated model:
    - Vehicle: Vehicle Insurance Fraud Detection
    - Bank: Bank Account Fraud Detection
    - Ecommerce: E-commerce Fraud Detection
    - Ethereum: Blockchain/Ethereum Fraud Detection
    
    Models output binary (0 or 1), converted to probability and fraud score (0-100).
    """
    
    def __init__(self):
        """Load all 4 models."""
        self.models = {
            "vehicle": load_model_vehicle(),
            "bank": load_model_bank(),
            "ecommerce": load_model_ecommerce(),
            "ethereum": load_model_eth()
        }
        self.transforms = {
            "vehicle": transform_vehicle_fraud_data,
            "bank": transform_bank_fraud_data,
            "ecommerce": transform_ecommerce_fraud_data,
            "ethereum": transform_eth_fraud_data
        }
    
    def _convert_to_probability(self, prediction: int) -> float:
        """
        Convert binary model output (0 or 1) to probability (0.0-1.0).
        
        - 0 (non-fraud) → 0.25 (low fraud probability)
        - 1 (fraud) → 0.75 (high fraud probability)
        
        Args:
            prediction: Binary output from model (0 or 1)
        
        Returns:
            Probability value between 0.0 and 1.0
        """
        return 0.25 if prediction == 0 else 0.75
    
    def _probability_to_score(self, probability: float) -> int:
        """
        Convert probability (0.0-1.0) to fraud score (0-100).
        
        Args:
            probability: Probability value
        
        Returns:
            Fraud score between 0 and 100
        """
        score = int(probability * 100)
        return max(0, min(100, score))
    
    def _get_risk_level(self, fraud_score: int) -> str:
        """
        Categorize risk level based on fraud score.
        
        Args:
            fraud_score: Score 0-100
        
        Returns:
            Risk level: LOW, MEDIUM, HIGH, or CRITICAL
        """
        if fraud_score < 25:
            return "LOW"
        elif fraud_score < 50:
            return "MEDIUM"
        elif fraud_score < 75:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def detect_fraud(self, transaction_data: Dict, transaction_type: str) -> Dict:
        """
        Detect fraud for a single transaction using appropriate model.
        
        Pipeline:
        1. Select model based on transaction_type
        2. Transform raw data using type-specific transformer
        3. Get binary prediction from model
        4. Convert to probability
        5. Convert to fraud score (0-100)
        6. Determine risk level
        
        Args:
            transaction_data: Raw transaction features as dictionary
            transaction_type: One of "vehicle", "bank", "ecommerce", "ethereum"
        
        Returns:
            Dictionary with fraud_score, probability, risk_level, and raw_prediction
        
        Raises:
            ValueError: If transaction_type is not recognized
        """
        if transaction_type not in self.models:
            raise ValueError(f"Unknown transaction type: {transaction_type}")
        
        try:
            # Load model and transform function
            model, features = self.models[transaction_type]
            transform_fn = self.transforms[transaction_type]
            
            # Convert to DataFrame
            df = pd.DataFrame([transaction_data])
            
            # Transform data
            transformed_data = transform_fn(df, features)
            
            # Get prediction from model
            raw_prediction = model.predict(transformed_data)[0]
            
            # Convert to probability
            probability = self._convert_to_probability(int(raw_prediction))
            
            # Convert to fraud score
            fraud_score = self._probability_to_score(probability)
            
            # Get risk level
            risk_level = self._get_risk_level(fraud_score)
            
            return {
                "fraud_score": fraud_score,
                "probability": probability,
                "risk_level": risk_level,
                "raw_prediction": int(raw_prediction),
                "transaction_type": transaction_type,
                "success": True
            }
        
        except Exception as e:
            return {
                "fraud_score": 0,
                "probability": 0.0,
                "risk_level": "UNKNOWN",
                "raw_prediction": -1,
                "transaction_type": transaction_type,
                "success": False,
                "error": str(e)
            }


# Global service instance
_service = None


def initialize_service():
    """Initialize fraud detection service."""
    global _service
    _service = FraudDetectionService()


def get_service() -> FraudDetectionService:
    """Get or initialize the fraud detection service."""
    global _service
    if _service is None:
        initialize_service()
    return _service


def detect_fraud(transaction_data: Dict, transaction_type: str) -> Dict:
    """
    Main entry point for fraud detection.
    
    Args:
        transaction_data: Raw transaction features
        transaction_type: "vehicle", "bank", "ecommerce", or "ethereum"
    
    Returns:
        Detection result with fraud_score, risk_level, etc.
    """
    service = get_service()
    return service.detect_fraud(transaction_data, transaction_type)

