from datetime import datetime
from pathlib import Path
import json

from db import feedback_collection

TRANSACTION_JSON_PATH = Path("/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/fraud_explanations_full.json")

async def get_reason_by_transaction_id(tx_id: str) -> str | None:
    try:
        with open(TRANSACTION_JSON_PATH, "r") as f:
            transactions = json.load(f)

        for tx in transactions:
            if tx.get("id") == tx_id:
                return tx.get("reason")
    except Exception as e:
        print(f"Error reading transaction JSON: {e}")
    
    return None

# async def insert_feedback_auto_reason(feedback_data: dict):
#     feedback_data["timestamp"] = datetime.utcnow()
#     tx_id = feedback_data.get("transaction_id")
#     reason = await get_reason_by_transaction_id(tx_id)
#     feedback_data["reason"] = reason if reason else "Reason not found"
#     print(f"Inserting feedback: =================={feedback_data}")
#     await feedback_collection.insert_one(feedback_data)
