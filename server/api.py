
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime
import json

# Initialize FastAPI app
app = FastAPI(title="Sentinel Fraud API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
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

# Mock database (would be a real database in production)
# Sample transactions
transactions = [
    {
        "id": "T123456",
        "timestamp": "2025-04-07T09:15:30",
        "amount": 15000,
        "accountNumber": "8765432109",
        "transactionType": "wire",
        "score": 0.85,
        "reason": "Transaction T123456 was flagged because the amount of ₹15,000 exceeds typical daily averages by over 300% for this account. The transaction also occurred from an unusual IP address not previously associated with this account."
    },
    {
        "id": "T123457",
        "timestamp": "2025-04-07T10:23:45",
        "amount": 5999,
        "accountNumber": "7654321098",
        "transactionType": "card",
        "score": 0.62,
        "reason": "Transaction T123457 was flagged due to unusual merchant category. This account typically performs transactions in retail and grocery, but this payment was made to a high-risk merchant category in a foreign jurisdiction."
    },
    {
        "id": "T123458",
        "timestamp": "2025-04-07T14:56:12",
        "amount": 2500,
        "accountNumber": "6543210987",
        "transactionType": "online",
        "score": 0.35,
        "reason": "Transaction T123458 triggered a low-level alert due to being slightly outside normal spending patterns. The transaction amount is higher than average for this merchant type, but remains within reasonable bounds for the account history."
    },
    {
        "id": "T123459",
        "timestamp": "2025-04-06T18:34:22",
        "amount": 12500,
        "accountNumber": "5432109876",
        "transactionType": "atm",
        "score": 0.78,
        "reason": "Transaction T123459 was flagged as potentially fraudulent because this ATM withdrawal occurred in a location over 500km from the account holder's typical transaction area. Additionally, there were 3 failed PIN attempts before this successful transaction."
    },
    {
        "id": "T123460",
        "timestamp": "2025-04-06T11:45:33",
        "amount": 8750,
        "accountNumber": "4321098765",
        "transactionType": "pos",
        "score": 0.52,
        "reason": "Transaction T123460 raised moderate concern due to unusual timing. This transaction occurred at 11:45 PM, while the account holder typically makes purchases between 8 AM and 8 PM. The merchant category itself is not unusual for this customer."
    }
]

# In-memory storage for feedback
system_feedback = []
transaction_feedback = []

# Simple authentication (demo purposes only - use proper auth in production)
DEMO_USERS = {
    "admin": {
        "password": "admin123",
        "name": "Admin User"
    }
}

class LoginData(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: Optional[str] = None

# Auth endpoints
@app.post("/api/auth/login", response_model=LoginResponse)
async def login(data: LoginData):
    print(f"Login attempt: username={data.username}")  # For debugging
    user = DEMO_USERS.get(data.username)
    if user and user["password"] == data.password:
        print("Login successful")  # For debugging
        return {"success": True}
    print("Login failed")  # For debugging
    return {"success": False, "message": "Invalid credentials"}

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# Transaction endpoints
@app.get("/api/transactions", response_model=List[Transaction])
async def get_transactions():
    return transactions

# Feedback endpoints
@app.post("/api/feedback/transaction")
async def submit_transaction_feedback(feedback: TransactionFeedback):
    transaction_feedback.append({
        "transaction_id": feedback.transaction_id,
        "is_correct": feedback.is_correct,
        "feedback": feedback.feedback,
        "timestamp": datetime.now().isoformat()
    })
    return {"success": True, "message": "Feedback submitted successfully"}

@app.post("/api/feedback/system")
async def submit_system_feedback(feedback: FeedbackCreate):
    system_feedback.append({
        "category": feedback.category,
        "details": feedback.details,
        "timestamp": datetime.now().isoformat()
    })
    return {"success": True, "message": "System feedback submitted successfully"}

# Run the API with uvicorn
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
