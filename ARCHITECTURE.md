# FraudProof Ledger - System Architecture

## Overview
Single-transaction fraud detection system with 4 specialized models for different domains.

## Data Flow

```
Frontend (HTML Form)
    ↓
    | Select transaction_type (vehicle/bank/ecommerce/ethereum)
    | Submit transaction_data as JSON
    ↓
Backend POST /test/detect
    ↓
    | 1. Validate transaction_type
    | 2. Load model + transform function for type
    | 3. Transform raw transaction_data
    | 4. Run inference (binary: 0 or 1)
    | 5. Convert to probability (0.25 or 0.75)
    | 6. Convert to fraud_score (0-100)
    | 7. Determine risk_level (LOW/MEDIUM/HIGH/CRITICAL)
    ↓
Database (FraudLog)
    ↓
    | Store: fraud_score, risk_level, probability, raw_prediction
    | Store: transaction_type, tx_hash, transaction_data
    ↓
Blockchain (if fraud_score > 50)
    ↓
    | Log fraud to smart contract
    | Store blockchain_tx_hash in database
    ↓
Return FraudDetectionResult to Frontend
    ↓
Dashboard GET /dash/
    ↓
    | Fetch all fraud_logs from database
    | For each record with blockchain_tx_hash, fetch on-chain data
    | Return records to frontend
    ↓
Frontend displays fraud logs
```

## Models & Transforms

### 1. Vehicle Insurance Fraud
- **Model**: `load_model_vehicle()` → (model, features)
- **Transform**: `transform_vehicle_fraud_data(df, features)`
- **Input Fields**: 
  - months_as_customer, age, policy_annual_premium, number_of_vehicles

### 2. Bank Account Fraud
- **Model**: `load_model_bank()` → (model, features)
- **Transform**: `transform_bank_fraud_data(df, features)`
- **Input Fields**:
  - account_age_days, transaction_amount, transaction_frequency, average_daily_balance

### 3. E-commerce Fraud
- **Model**: `load_model_ecommerce()` → (model, features)
- **Transform**: `transform_ecommerce_fraud_data(df, features)`
- **Input Fields**:
  - purchase_amount, device_type, shipping_address_matches_billing, customer_age

### 4. Ethereum/Blockchain Fraud
- **Model**: `load_model_eth()` → (model, features)
- **Transform**: `transform_eth_fraud_data(df, features)`
- **Input Fields**:
  - transaction_value_eth, gas_price, contract_interaction, sender_transaction_count

## Backend Components

### Services

#### ai_service.py
```python
detect_fraud(transaction_data: Dict, transaction_type: str) -> Dict
```
- Loads appropriate model
- Transforms data
- Gets binary prediction (0 or 1)
- Converts to probability (0.25 for 0, 0.75 for 1)
- Converts to fraud_score (0-100)
- Returns: {fraud_score, probability, risk_level, raw_prediction, success}

### Routers

#### POST /test/detect
```json
{
  "transaction_type": "vehicle",
  "transaction_data": {
    "months_as_customer": 24,
    "age": 35,
    "policy_annual_premium": 1500.00,
    "number_of_vehicles": 2
  },
  "tx_hash": "optional_identifier"
}
```

Response:
```json
{
  "success": true,
  "fraud_score": 35,
  "risk_level": "MEDIUM",
  "probability": 0.35,
  "raw_prediction": 1,
  "transaction_type": "vehicle",
  "database_id": 1,
  "blockchain_tx": "0x..."
}
```

#### GET /dash/
Returns all fraud logs from database with optional blockchain data

#### GET /dash/{record_id}
Returns single fraud log with full details

#### GET /dash/type/{transaction_type}
Returns all logs for specific transaction type

### Database Model (FraudLog)
- **id**: Primary key
- **tx_hash**: Transaction identifier (unique)
- **transaction_type**: vehicle/bank/ecommerce/ethereum
- **fraud_score**: 0-100
- **risk_level**: LOW/MEDIUM/HIGH/CRITICAL
- **probability**: 0.0-1.0
- **raw_prediction**: 0 or 1
- **model_version**: v1
- **transaction_data**: JSON of original input
- **blockchain_tx_hash**: Hash of blockchain transaction (if logged)
- **created_at**: Timestamp

## Frontend

### test.html
- Form with radio buttons for transaction type selection
- Conditional fields based on selected type
- Submit → POST /test/detect
- Display fraud score gauge with color coding
- Show detection details (probability, risk level, etc.)
- Show database record ID and blockchain status

### dash.html
- Displays fraud logs from GET /dash/
- Shows fraud_score, risk_level, transaction_type
- Links to blockchain data (if available)
- Filters by transaction type

## Risk Levels
- **LOW** (0-25): Score < 25
- **MEDIUM** (25-50): Score 25-50
- **HIGH** (50-75): Score 50-75
- **CRITICAL** (75-100): Score > 75

## Blockchain Integration
- Frauds with score > 50 are logged to blockchain
- Stores features and fraud score in smart contract
- Database maintains reference to blockchain transaction
- Dashboard can fetch on-chain data via `get_onchain_fraud_data()`

## Key Design Decisions
1. **Single Model per Transaction**: Each type uses one dedicated model
2. **Binary to Probability**: Simple conversion (0→0.25, 1→0.75)
3. **Database First**: All results stored in DB, blockchain is optional
4. **Type-Specific Forms**: Frontend shows only relevant fields for selected type
5. **Threshold-Based Logging**: Only fraud_score > 50 goes to blockchain
