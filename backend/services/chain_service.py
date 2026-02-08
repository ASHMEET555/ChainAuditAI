import json
from web3 import Web3
from core.web3_client import w3, contract
from core.config import PRIVATE_KEY 

def get_onchain_fraud_data(tx_hash: str):
    """Read fraud data from blockchain."""
    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        block = w3.eth.get_block(receipt.blockNumber)
        events = contract.events.FraudLogged().process_receipt(receipt)
        if not events: return None
        event = events[0]["args"]
        return {
            "fraud_score": event["fraudScore"],
            "model_version": event["modelVersion"],
            "timestamp": block.timestamp,
            "gas_used": receipt.gasUsed,
            "tx_hash": tx_hash
        }
    except Exception as e:
        print(f"Error fetching chain data: {e}")
        return None

def log_fraud_on_chain(fraud_score: int, model_version: str, reference_id: str):
    """
    Write fraud record to blockchain.
    """
    if not contract:
        print("Error: Contract not initialized.")
        return None
    
    if not PRIVATE_KEY:
        print("Error: PRIVATE_KEY not found in config.")
        return None

    try:
        # 1. Derive Sender Address
        account = w3.eth.account.from_key(PRIVATE_KEY)
        sender_address = account.address
        
        # 2. Convert Reference ID (String) to Bytes32 (Hash)
        # Solidity 'bytes32' requires a fixed-length 32-byte hash
        tx_hash_bytes = w3.keccak(text=reference_id)
        
        print(f"Mining transaction for Ref ID: {reference_id}...")
        
        # 3. Build Transaction (CORRECTED ORDER: Hash -> Score -> Version)
        tx = contract.functions.logFraud(
            tx_hash_bytes,       # Arg 1: bytes32 _transactionHash
            int(fraud_score),    # Arg 2: uint256 _fraudScore
            str(model_version)   # Arg 3: string memory _modelVersion
        ).build_transaction({
            'from': sender_address,
            'nonce': w3.eth.get_transaction_count(sender_address),
            'gas': 2000000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })

        # 4. Sign Transaction
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

        # 5. Send Transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        # 6. Wait for Receipt
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction mined: {receipt.transactionHash.hex()}")
        
        return receipt.transactionHash.hex()

    except Exception as e:
        print(f"Blockchain Write Error: {e}")
        # Debugging aid
        import traceback
        traceback.print_exc()
        return None