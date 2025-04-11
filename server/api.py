
# from pathlib import Path
# from fastapi import FastAPI, HTTPException, Depends, status
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Optional
# import uvicorn
# import os
# import pandas as pd
# import json
# from datetime import datetime
# import json
# from modules.combine import merge_parquet_to_csv
# from modules.transformation import enrich_with_historical_features
# from modules.rule_based_fraud_detection import apply_rule_based_fraud_detection
# from modules.history import generate_account_level_history
# from modules.model import run_autoencoder_fraud_detection
# from modules.gemini_llm import generate_fraud_explanations

# fraud_explanations_cache = []

# # Initialize FastAPI app
# app = FastAPI(title="Sentinel Fraud API")

# # Enable CORS for frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, replace with specific origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Data Models
# class FeedbackCreate(BaseModel):
#     category: str
#     details: str

# class TransactionFeedback(BaseModel):
#     transaction_id: str
#     is_correct: bool
#     feedback: Optional[str] = None

# class Transaction(BaseModel):
#     id: str
#     timestamp: str
#     amount: float
#     accountNumber: str
#     transactionType: str
#     score: float
#     reason: str


# # def load_fraud_explanations(path="/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/fraud_explanations_full.json"):
# #     try:
# #         with open(path, "r") as f:
# #             data = json.load(f)
# #             return data
# #     except FileNotFoundError:
# #         print(f"⚠️ File not found: {path}")
# #         return []
    
# def load_fraud_explanations(path="/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/fraud_explanations_full.json"):
#     try:
#         with open(path, "r") as f:
#             data = json.load(f)
#             return data
#     except FileNotFoundError:
#         print(f"⚠️ File not found: {path}")
#         return []
    
# def append_to_fraud_explanations(
#     new_fraud_json_path: str,
#     full_explanations_path: str
# ):
#     try:
#         # Load new fraud transactions (no LLM reason yet)
#         with open(new_fraud_json_path, "r") as f:
#             new_frauds = json.load(f)

#         # Load existing explanations (if exists)
#         if Path(full_explanations_path).exists():
#             with open(full_explanations_path, "r") as f:
#                 existing_explanations = json.load(f)
#         else:
#             existing_explanations = []

#         # Create a set of existing IDs for fast lookup
#         existing_ids = {entry["id"] for entry in existing_explanations}

#         # Append only new entries
#         new_entries = [
#             tx for tx in new_frauds
#             if tx["id"] not in existing_ids
#         ]

#         print(f"➕ Appending {len(new_entries)} new fraud entries to explanations JSON")

#         # Combine and save
#         combined = existing_explanations + new_entries

#         with open(full_explanations_path, "w") as f:
#             json.dump(combined, f, indent=2)

#         print(f"✅ Total entries in '{full_explanations_path}': {len(combined)}")

#     except Exception as e:
#         print(f"❌ Failed to append to fraud explanations: {e}")

# # Mock database (would be a real database in production)
# # Sample transactions
# # transactions = [
# #     {
# #         "id": "T123456",
# #         "timestamp": "2025-04-07T09:15:30",
# #         "amount": 25000,
# #         "accountNumber": "8765432109",
# #         "transactionType": "wire",
# #         "score": 0.85,
# #         "reason": "Transaction T123456 was flagged because the amount of ₹15,000 exceeds typical daily averages by over 300% for this account. The transaction also occurred from an unusual IP address not previously associated with this account."
# #     },
# #     {
# #         "id": "T123457",
# #         "timestamp": "2025-04-07T10:23:45",
# #         "amount": 5999,
# #         "accountNumber": "7654321098",
# #         "transactionType": "card",
# #         "score": 0.62,
# #         "reason": "Transaction T123457 was flagged due to unusual merchant category. This account typically performs transactions in retail and grocery, but this payment was made to a high-risk merchant category in a foreign jurisdiction."
# #     },
# #     {
# #         "id": "T123458",
# #         "timestamp": "2025-04-07T14:56:12",
# #         "amount": 2500,
# #         "accountNumber": "6543210987",
# #         "transactionType": "online",
# #         "score": 0.35,
# #         "reason": "Transaction T123458 triggered a low-level alert due to being slightly outside normal spending patterns. The transaction amount is higher than average for this merchant type, but remains within reasonable bounds for the account history."
# #     },
# #     {
# #         "id": "T123459",
# #         "timestamp": "2025-04-06T18:34:22",
# #         "amount": 12500,
# #         "accountNumber": "5432109876",
# #         "transactionType": "atm",
# #         "score": 0.78,
# #         "reason": "Transaction T123459 was flagged as potentially fraudulent because this ATM withdrawal occurred in a location over 500km from the account holder's typical transaction area. Additionally, there were 3 failed PIN attempts before this successful transaction."
# #     },
# #     {
# #         "id": "T123460",
# #         "timestamp": "2025-04-06T11:45:33",
# #         "amount": 8750,
# #         "accountNumber": "4321098765",
# #         "transactionType": "pos",
# #         "score": 0.52,
# #         "reason": "Transaction T123460 raised moderate concern due to unusual timing. This transaction occurred at 11:45 PM, while the account holder typically makes purchases between 8 AM and 8 PM. The merchant category itself is not unusual for this customer."
# #     }
# # ]

# # In-memory storage for feedback
# system_feedback = []
# transaction_feedback = []

# # Simple authentication (demo purposes only - use proper auth in production)
# DEMO_USERS = {
#     "admin": {
#         "password": "admin123",
#         "name": "Admin User"
#     }
# }

# class LoginData(BaseModel):
#     username: str
#     password: str

# class LoginResponse(BaseModel):
#     success: bool
#     message: Optional[str] = None

# @app.on_event("startup")
# def startup_event():
#     print("🚀 Starting FastAPI server... Running data denormalization.")
#     # merge_parquet_to_csv()
#     # enrich_with_historical_features('csv')
#     output_dir = merge_parquet_to_csv()

#     enrich_with_historical_features(output_dir)
#     # apply_rule_based_fraud_detection(os.path.join(output_dir, "denoised_enriched_transactions.csv"))
#     transaction=apply_rule_based_fraud_detection(os.path.join(output_dir, "denoised_enriched_transactions.csv"))

#     generate_account_level_history(output_dir)
#     run_autoencoder_fraud_detection()
#     generate_fraud_explanations() 

#     # Load fraud explanations to memory
#     # global fraud_explanations_cache
#     # fraud_explanations_cache = load_fraud_explanations()
#     # print(f"✅ Loaded {len(fraud_explanations_cache)} fraud explanations into memory.")
#     global fraud_explanations_cache
#     append_to_fraud_explanations(
#         "/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/fraud_transactions.json",
#         "/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/fraud_explanations_full.json"
#     )

#     print(f"✅ Loaded {len(fraud_explanations_cache)} combined fraud transactions into memory.")
    
# @app.get("/")
# def read_root():
#     return {"message": "FastAPI is running with Spark integration"}

# # Auth endpoints
# @app.post("/api/auth/login", response_model=LoginResponse)
# async def login(data: LoginData):
#     print(f"Login attempt: username={data.username}")  # For debugging
#     user = DEMO_USERS.get(data.username)
#     if user and user["password"] == data.password:
#         print("Login successful")  # For debugging
#         return {"success": True}
#     print("Login failed")  # For debugging
#     return {"success": False, "message": "Invalid credentials"}

# # Health check endpoint
# @app.get("/api/health")
# async def health_check():
#     return {"status": "ok", "timestamp": datetime.now().isoformat()}

# # Transaction endpoints
# @app.get("/api/transactions", response_model=List[Transaction])
# async def get_transactions():
#     return fraud_explanations_cache


# # Feedback endpoints
# @app.post("/api/feedback/transaction")
# async def submit_transaction_feedback(feedback: TransactionFeedback):
#     transaction_feedback.append({
#         "transaction_id": feedback.transaction_id,
#         "is_correct": feedback.is_correct,
#         "feedback": feedback.feedback,
#         "timestamp": datetime.now().isoformat()
#     })
#     return {"success": True, "message": "Feedback submitted successfully"}

# @app.post("/api/feedback/system")
# async def submit_system_feedback(feedback: FeedbackCreate):
#     system_feedback.append({
#         "category": feedback.category,
#         "details": feedback.details,
#         "timestamp": datetime.now().isoformat()
#     })
#     return {"success": True, "message": "System feedback submitted successfully"}

# # Run the API with uvicorn
# if __name__ == "__main__":
#     uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)



from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import pandas as pd
import json
from datetime import datetime
# from crud import insert_feedback_auto_reason
from db import feedback_collection
# Module imports
from modules.combine import merge_parquet_to_csv
from modules.transformation import enrich_with_historical_features
from modules.rule_based_fraud_detection import apply_rule_based_fraud_detection
from modules.history import generate_account_level_history
from modules.model import run_autoencoder_fraud_detection
from modules.gemini_llm import generate_fraud_explanations
from db import insert_feedback_auto_reason
fraud_explanations_cache = []

# Initialize FastAPI app
app = FastAPI(title="Sentinel Fraud API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------- Models ----------------------------

class FeedbackCreate(BaseModel):
    category: str
    details: str

class TransactionFeedback(BaseModel):
    transaction_id: str
    is_correct: bool
    feedback: Optional[str] = None

class Transaction(BaseModel):
    id: str
    timestamp: str
    amount: float
    accountNumber: str
    transactionType: str
    score: float
    reason: str

class LoginData(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: Optional[str] = None

# ---------------------------- Auth ----------------------------

DEMO_USERS = {
    "admin": {
        "password": "admin123",
        "name": "Admin User"
    }
}

# ------------------------ Utility Functions ------------------------

def load_fraud_explanations(path: str) -> list:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ File not found: {path}")
        return []

def update_cache_reason(transaction_id: str, new_reason: str):
    for tx in fraud_explanations_cache:
        if tx["id"] == transaction_id:
            tx["reason"] = new_reason  # update directly
            print(f"🧠 In-memory cache updated for {transaction_id} with: {new_reason}")
            return

def append_to_fraud_explanations(new_fraud_json_path: str, full_explanations_path: str):
    try:
        with open(new_fraud_json_path, "r") as f:
            new_frauds = json.load(f)

        if Path(full_explanations_path).exists():
            with open(full_explanations_path, "r") as f:
                existing_explanations = json.load(f)
        else:
            existing_explanations = []

        existing_ids = {entry["id"] for entry in existing_explanations}
        new_entries = [tx for tx in new_frauds if tx["id"] not in existing_ids]

        print(f"➕ Appending {len(new_entries)} new fraud entries to explanations JSON")

        combined = existing_explanations + new_entries

        with open(full_explanations_path, "w") as f:
            json.dump(combined, f, indent=2)

        print(f"✅ Total entries in '{full_explanations_path}': {len(combined)}")

    except Exception as e:
        print(f"❌ Failed to append to fraud explanations: {e}")

# ------------------------ Server Startup ------------------------

@app.on_event("startup")
def startup_event():
    global fraud_explanations_cache

    print("🚀 Starting FastAPI server... Running data processing pipeline.")
    
    output_dir = merge_parquet_to_csv()
    enrich_with_historical_features(output_dir)

    input_csv = os.path.join(output_dir, "denoised_enriched_transactions.csv")
    apply_rule_based_fraud_detection(input_csv)

    generate_account_level_history(output_dir)
    run_autoencoder_fraud_detection()
    generate_fraud_explanations() 

    # Append new frauds to the full JSON
    fraud_json_path = "/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/fraud_transactions.json"
    full_json_path = "/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/fraud_explanations_full.json"
    append_to_fraud_explanations(fraud_json_path, full_json_path)

    # Load full data into memory for API
    fraud_explanations_cache = load_fraud_explanations(full_json_path)
    print(f"✅ Loaded {len(fraud_explanations_cache)} fraud transactions into memory.")

# ------------------------ Routes ------------------------

@app.get("/")
def read_root():
    return {"message": "FastAPI is running with Spark integration"}

@app.post("/api/auth/login", response_model=LoginResponse)
async def login(data: LoginData):
    print(f"Login attempt: username={data.username}")
    user = DEMO_USERS.get(data.username)
    if user and user["password"] == data.password:
        return {"success": True}
    return {"success": False, "message": "Invalid credentials"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/api/transactions", response_model=List[Transaction])
async def get_transactions():
    return fraud_explanations_cache

# Feedback
system_feedback = []
transaction_feedback = []


# async def insert_feedback_auto_reason(feedback_dict):
#     session = SessionLocal()

#     # 1. Save feedback to DB
#     feedback = FeedbackModel(
#         transaction_id=feedback_dict["transaction_id"],
#         is_correct=feedback_dict["is_correct"],
#         feedback=feedback_dict.get("feedback")
#     )
#     session.merge(feedback)
#     session.commit()

#     # 2. If incorrect, regenerate and update
#     if not feedback.is_correct:
#         new_reason = regenerate_explanation_for_transaction(feedback.transaction_id)
#         update_json_explanation(feedback.transaction_id, new_reason)
#         print(f"♻️ Auto-regenerated and updated explanation for {feedback.transaction_id}")
#     else:
#         print(f"✅ Feedback marked correct for {feedback.transaction_id}, no action.")


# @app.post("/api/feedback/transaction")
# async def submit_feedback(feedback: TransactionFeedback):
#     print("📩 Feedback endpoint hit with:", feedback.dict())
#     await insert_feedback_auto_reason(feedback.dict())
#     return {"success": True, "message": "Feedback saved with reason"}

# @app.post("/api/feedback/transaction")
# async def submit_feedback(feedback: TransactionFeedback):
#     print("📩 Feedback endpoint hit with:", feedback.dict())
#     await insert_feedback_auto_reason(feedback.dict())
#     return {"success": True, "message": "Feedback saved with reason"}


@app.post("/api/feedback/transaction")
async def submit_feedback(feedback: TransactionFeedback):
    print("📩 Feedback endpoint hit with:", feedback.dict())

    # Inject cache update logic
    await insert_feedback_auto_reason(
        feedback.dict(),
        cache_updater=update_cache_reason  # 💥 add this
    )

    return {"success": True, "message": "Feedback saved with reason"}

# @app.post("/api/feedback/transaction")
# async def submit_feedback(feedback: TransactionFeedback):
#     print("📩 Feedback endpoint hit with:", feedback.dict())
#     try:
#         await insert_feedback_auto_reason(
#             feedback.dict(),
#             cache_updater=update_cache_reason
#         )
#         return {"success": True, "message": "Feedback saved with reason"}
#     except Exception as e:
#         print(f"❌ Error in feedback submission: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/feedback/transaction/{transaction_id}", response_model=List[TransactionFeedback])
async def get_feedback_by_transaction(transaction_id: str):
    feedback_list = []
    seen = set()

    async for feedback in feedback_collection.find({"transaction_id": transaction_id}):
        feedback["id"] = str(feedback["_id"])
        del feedback["_id"]

        # Key based on feedback content and correctness
        feedback_key = (
            feedback.get("feedback", "").strip().lower(),
            feedback.get("is_correct", False)
        )

        if feedback_key not in seen:
            seen.add(feedback_key)
            feedback_list.append(feedback)

    if not feedback_list:
        raise HTTPException(status_code=404, detail="No feedback found for this transaction")

    return feedback_list


@app.post("/api/feedback/system")
async def submit_system_feedback(feedback: FeedbackCreate):
    system_feedback.append({
        "category": feedback.category,
        "details": feedback.details,
        "timestamp": datetime.now().isoformat()
    })
    return {"success": True, "message": "System feedback submitted successfully"}

# ------------------------ Run the Server ------------------------

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
