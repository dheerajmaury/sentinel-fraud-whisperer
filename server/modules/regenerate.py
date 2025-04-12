# modules/regenerate.py
import pandas as pd
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="your_api_key_here")
model = genai.GenerativeModel("gemini-1.5-pro")

def regenerate_explanation_for_transaction(transaction_id: str, reviewer_feedback: str = "") -> str:
    base_dir = Path(__file__).resolve().parent.parent
    csv_path = base_dir / "fraud_cases_for_llm.csv"
    history_path = base_dir / "denormalized_transactions/account_history.csv"

    fraud_cases = pd.read_csv(csv_path)
    account_history = pd.read_csv(history_path)

    merged = fraud_cases.merge(account_history, on="account_id", how="left", suffixes=('', '_history'))
    row = merged[merged["transaction_id"] == transaction_id].iloc[0]

    transaction_info = row.drop(labels=[col for col in row.index if col.endswith('_history') or col == "score"]).to_dict()
    history_info = {k: v for k, v in row.to_dict().items() if k.endswith('_history')}

    prompt = f"""
You are an AI fraud analyst. A reviewer marked the model's fraud reason incorrect and provided feedback.

--- Transaction Info ---
{transaction_info}

--- Account History Info ---
{history_info}

--- Reviewer Feedback ---
{reviewer_feedback}

Now, generate a new concise fraud reason based on the above context and feedback.
Return ONLY the revised reason, no explanation or comments.
"""

    response = model.generate_content(prompt)
    return response.text.strip()
