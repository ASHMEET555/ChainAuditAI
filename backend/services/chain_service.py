from core.web3_client import w3, contract

def get_onchain_fraud_data(tx_hash: str):
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    block = w3.eth.get_block(receipt.blockNumber)

    events = contract.events.FraudLogged().process_receipt(receipt)
    event = events[0]["args"]

    return {
        "fraud_score": event["fraudScore"],
        "model_version": event["modelVersion"],
        "timestamp": block.timestamp,
        "gas_used": receipt.gasUsed
    }
