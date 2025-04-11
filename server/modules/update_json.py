# modules/update_json.py
import json
from pathlib import Path

def update_json_explanation(transaction_id: str, new_reason: str):
    json_path = Path(__file__).resolve().parent.parent / "fraud_explanations_full.json"

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return

    updated = False
    for item in data:
        if str(item.get("id")).strip() == str(transaction_id).strip():
            print(f"🔄 Updating reason for transaction: {transaction_id}")
            item["reason"] = new_reason
            updated = True
            break

    if updated:
        try:
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"✅ Explanation updated in JSON for {transaction_id}")
        except Exception as e:
            print(f"❌ Failed to write updated JSON: {e}")
    else:
        print(f"⚠️ Transaction ID {transaction_id} not found in JSON.")
