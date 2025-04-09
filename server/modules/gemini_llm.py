# import pandas as pd

# import json

# from google import genai
 
# # Load data

# fraud_cases = pd.read_csv("fraud_cases_for_llm.csv")

# account_history = pd.read_csv("account_history.csv")
 
# # Merge on account_id to get history

# if "account_id" not in fraud_cases.columns or "account_id" not in account_history.columns:

#     raise ValueError("Both CSV files must contain 'account_id' column.")
 
# merged = fraud_cases.merge(account_history, on="account_id", how="left", suffixes=('', '_history'))
 
# # Normalize anomaly scores for interpretability

# min_score = fraud_cases["anomaly_score"].min()

# max_score = fraud_cases["anomaly_score"].max()

# fraud_cases["score"] = (fraud_cases["anomaly_score"] - min_score) / (max_score - min_score)
 
# # Merge updated scores back to merged DataFrame

# merged["score"] = fraud_cases["score"]
 
# # Set up Gemini client

# client = genai.Client(api_key="your_api_key_here")  # Replace with your actual API key
 
# # Function to generate explanation for each fraud case

# def get_explanation(row):

#     transaction_info = row.drop(labels=[col for col in row.index if col.endswith('_history') or col == "score"]).to_dict()

#     history_info = {k: v for k, v in row.to_dict().items() if k.endswith('_history')}
 
#     prompt = f"""

# You are an AI fraud analyst. A fraud detection model flagged the following transaction as fraud:
 
# --- Transaction Info ---

# {transaction_info}
 
# --- Account History Info ---

# {history_info}
 
# Provide a 2-line explanation of why the model might have flagged this transaction.

# """

#     response = client.models.generate_content(

#         model="gemini-2.0-flash",

#         contents=prompt

#     )

#     return response.text.strip()
 
# # Build results

# transactions = []
 
# for idx, row in merged.iterrows():

#     try:

#         explanation = get_explanation(row)

#     except Exception as e:

#         explanation = f"Error: {e}"
 
#     transaction_entry = {

#         "id": row.get("transaction_id", f"T{idx}"),

#         "timestamp": row.get("timestamp"),

#         "amount": row.get("amount"),

#         "accountNumber": row.get("account_number"),

#         "transactionType": row.get("transaction_type"),

#         "score": float(row["score"]),

#         "reason": explanation

#     }

#     transactions.append(transaction_entry)
 
# # Save all fraud explanations

# with open("fraud_explanations_full.json", "w") as f:

#     json.dump(transactions, f, indent=2)
 
# print("✅ Saved all fraud explanations to 'fraud_explanations_full.json'")

 
# return     transactions
 


# server/modules/fraud_explanation.py
from pathlib import Path
import pandas as pd
import json
# import google.generativeai as genai 
import google.generativeai as genai


def generate_fraud_explanations():
    print("🤖 Generating Gemini explanations...")
    base_dir = Path(__file__).resolve().parent.parent  # Go to project root
    csv_path = base_dir / "fraud_cases_for_llm.csv"
    # fraud_path = "server/fraud_cases_for_llm.csv"
    # history_path = "server/denormalized_transactions/account_history.csv"
    history_path = base_dir / "denormalized_transactions/account_history.csv"   
    output_path = base_dir/"fraud_explanations_full.json"

    # Load data
    fraud_cases = pd.read_csv(csv_path)
    account_history = pd.read_csv(history_path)

    if "account_id" not in fraud_cases.columns or "account_id" not in account_history.columns:
        raise ValueError("Missing 'account_id' column in one of the inputs.")

    # Merge
    merged = fraud_cases.merge(account_history, on="account_id", how="left", suffixes=('', '_history'))

    # Normalize anomaly scores
    min_score = fraud_cases["anomaly_score"].min()
    max_score = fraud_cases["anomaly_score"].max()
    fraud_cases["score"] = (fraud_cases["anomaly_score"] - min_score) / (max_score - min_score)
    merged["score"] = fraud_cases["score"]

    # Gemini client
    genai.configure(api_key="yAIzaSyDfd_TYPR0jI9E-UNTSPecEYYYP1Ewft60")
    model = genai.GenerativeModel("gemini-1.5-pro")
    # client = genai.Client(api_key="yAIzaSyDfd_TYPR0jI9E-UNTSPecEYYYP1Ewft60")  # Replace with actual key

    def get_explanation(row):
        transaction_info = row.drop(labels=[col for col in row.index if col.endswith('_history') or col == "score"]).to_dict()
        history_info = {k: v for k, v in row.to_dict().items() if k.endswith('_history')}

        prompt = f"""
You are an AI fraud analyst. A fraud detection model flagged the following transaction as fraud:

--- Transaction Info ---
{transaction_info}

--- Account History Info ---
{history_info}

Provide a 2-line explanation of why the model might have flagged this transaction.
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text.strip()

    # Build explanations
    transactions = []

    for idx, row in merged.iterrows():
        try:
            explanation = get_explanation(row)
        except Exception as e:
            explanation = f"Error: {e}"

        transactions.append({
            "id": row.get("transaction_id", f"T{idx}"),
            "timestamp": row.get("timestamp"),
            "amount": row.get("amount"),
            "accountNumber": row.get("account_number"),
            "transactionType": row.get("transaction_type"),
            "score": float(row["score"]),
            "reason": explanation
        })

    with open(output_path, "w") as f:
        json.dump(transactions, f, indent=2)

    print(f"✅ Saved {len(transactions)} fraud explanations to '{output_path}'")
