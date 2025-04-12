


from motor.motor_asyncio import AsyncIOMotorClient
from modules.regenerate import regenerate_explanation_for_transaction
from modules.update_json import update_json_explanation
from datetime import datetime

MONGO_URL = "Mongodb connection "
client = AsyncIOMotorClient(MONGO_URL)
db = client["feedback_db"]
feedback_collection = db["feedback"]

async def insert_feedback_auto_reason(feedback_dict, cache_updater=None):
    feedback_dict["timestamp"] = datetime.now()

    if not feedback_dict["is_correct"]:
        new_reason = regenerate_explanation_for_transaction(
            feedback_dict["transaction_id"],
            feedback_dict.get("feedback", "")
        )
        feedback_dict["reason"] = new_reason

        # Update JSON file
        update_json_explanation(feedback_dict["transaction_id"], new_reason)

        # Update in-memory cache if updater provided
        if cache_updater:
            print("🔁 Updating in-memory cache...")
            cache_updater(feedback_dict["transaction_id"], new_reason)

        print(f"♻️ Auto-regenerated and updated reason for {feedback_dict['transaction_id']}")
    else:
        print(f"✅ Feedback marked correct for {feedback_dict['transaction_id']}, no reason change.")

    await feedback_collection.insert_one(feedback_dict)
    print("✅ Feedback saved:", feedback_dict)


