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

 
# # # return     transactions
 


# # server/modules/fraud_explanation.py# server/modules/fraud_explanation.py
# from pathlib import Path
# import pandas as pd
# import json
# import time
# import google.generativeai as genai

# def generate_fraud_explanations():
#     print("🤖 Generating Gemini explanations...")

#     # Paths
#     base_dir = Path(__file__).resolve().parent.parent
#     csv_path = base_dir / "fraud_cases_for_llm.csv"
#     history_path = base_dir / "denormalized_transactions/account_history.csv"
#     output_path = base_dir / "fraud_explanations_full.json"

#     # Load data
#     fraud_cases = pd.read_csv(csv_path)
#     account_history = pd.read_csv(history_path)

#     # Ensure required columns
#     if "account_id" not in fraud_cases.columns or "account_id" not in account_history.columns:
#         raise ValueError("Missing 'account_id' column in one of the inputs.")

#     # Normalize scores
#     min_score = fraud_cases["anomaly_score"].min()
#     max_score = fraud_cases["anomaly_score"].max()
#     fraud_cases["score"] = (fraud_cases["anomaly_score"] - min_score) / (max_score - min_score)

#     # Merge and get top 3
#     # merged = fraud_cases.merge(account_history, on="account_id", how="left", suffixes=('', '_history'))
#     # merged["score"] = fraud_cases["score"]
#     # merged = merged.sort_values(by="score", ascending=False).head(3)
#     # Sort by score descending
#     fraud_cases_sorted = fraud_cases.sort_values(by="score", ascending=False)

# # Keep only the top transaction per unique account
#     top_unique_accounts = fraud_cases_sorted.drop_duplicates(subset="account_id").head(3)

# # Merge with account history
#     merged = top_unique_accounts.merge(account_history, on="account_id", how="left", suffixes=('', '_history'))

#     # Configure Gemini client
#     genai.configure(api_key="your_api_key_here")  # Replace with your actual API key
#     model = genai.GenerativeModel("gemini-1.5-pro")

#     def get_explanation(row):
#         transaction_info = row.drop(labels=[col for col in row.index if col.endswith('_history') or col == "score"]).to_dict()
#         history_info = {k: v for k, v in row.to_dict().items() if k.endswith('_history')}

#         prompt = f"""
# You are an AI fraud analyst. A fraud detection model flagged the following transaction as fraud:

# --- Transaction Info ---
# {transaction_info}

# --- Account History Info ---
# {history_info}

# Provide a 2-line explanation of why the model might have flagged this transaction.
# """
#         response = model.generate_content(prompt)
#         return response.text.strip()

#     # Generate explanations
#     transactions = []

#     for idx, row in merged.iterrows():
#         try:
#             explanation = get_explanation(row)
#         except Exception as e:
#             explanation = f"Error: {e}"

#         print(f"\n📝 Explanation for transaction {row.get('transaction_id', f'T{idx}')}: {explanation}\n")

#         transactions.append({
#             "id": row.get("transaction_id", f"T{idx}"),
#             "timestamp": row.get("timestamp"),
#             "amount": row.get("amount"),
#             "accountNumber": row.get("account_number"),
#             "transactionType": row.get("transaction_type"),
#             "score": float(row["score"]),
#             "reason": explanation
#         })
#   # Delay between API calls

#     # Save to JSON
#     with open(output_path, "w") as f:
#         json.dump(transactions, f, indent=2)

#     print(f"✅ Saved {len(transactions)} fraud explanations to '{output_path}'")

# server/modules/fraud_explanation.py
# from pathlib import Path
# import pandas as pd
# import json
# import time
# import google.generativeai as genai

# def generate_fraud_explanations():
#     print("🤖 Generating Gemini explanations...")

#     # Paths
#     base_dir = Path(__file__).resolve().parent.parent
#     csv_path = base_dir / "fraud_cases_for_llm.csv"
#     history_path = base_dir / "denormalized_transactions/account_history.csv"
#     output_path = base_dir / "fraud_explanations_full.json"

#     # Load data
#     fraud_cases = pd.read_csv(csv_path)
#     account_history = pd.read_csv(history_path)

#     # Ensure required columns
#     if "account_id" not in fraud_cases.columns or "account_id" not in account_history.columns:
#         raise ValueError("Missing 'account_id' column in one of the inputs.")

#     # Normalize scores
#     min_score = fraud_cases["anomaly_score"].min()
#     max_score = fraud_cases["anomaly_score"].max()
#     fraud_cases["score"] = (fraud_cases["anomaly_score"] - min_score) / (max_score - min_score)

#     # Merge and get top 3
#     # merged = fraud_cases.merge(account_history, on="account_id", how="left", suffixes=('', '_history'))
#     # merged["score"] = fraud_cases["score"]
#     # merged = merged.sort_values(by="score", ascending=False).head(3)
#     # Sort by score descending
#     fraud_cases_sorted = fraud_cases.sort_values(by="score", ascending=False)

# # Keep only the top transaction per unique account
#     top_unique_accounts = fraud_cases_sorted.drop_duplicates(subset="account_id").head(3)

# # Merge with account history
#     merged = top_unique_accounts.merge(account_history, on="account_id", how="left", suffixes=('', '_history'))


#     # Configure Gemini client
#     genai.configure(api_key="your_api_key_here")  # Replace with your actual API key
#     model = genai.GenerativeModel("gemini-1.5-pro")

#     def get_explanation(row):
#         transaction_info = row.drop(labels=[col for col in row.index if col.endswith('_history') or col == "score"]).to_dict()
#         history_info = {k: v for k, v in row.to_dict().items() if k.endswith('_history')}

#         prompt = f"""
# You are an expert fraud analyst.

# A transaction has been flagged as potentially fraudulent.

# Analyze the transaction and account history below and give a **precise 1-2 sentence reason** why this might be fraud. Be direct and specific. Avoid generalities.

# --- Transaction Info ---
# {transaction_info}

# --- Account History Info ---
# {history_info}

# Explain why this transaction is likely fraudulent:
# """
#         response = model.generate_content(prompt)
#         return response.text.strip()

#     # Generate explanations
#     transactions = []

#     for idx, row in merged.iterrows():
#         try:
#             explanation = get_explanation(row)
#         except Exception as e:
#             explanation = f"Error: {e}"

#         print(f"\n📝 Explanation for transaction {row.get('transaction_id', f'T{idx}')}: {explanation}\n")

#         transactions.append({
#             "id": row.get("transaction_id", f"T{idx}"),
#             "timestamp": row.get("timestamp"),
#             "amount": row.get("amount"),
#             "accountNumber": row.get("account_number"),
#             "transactionType": row.get("transaction_type"),
#             "score": float(row["score"]),
#             "reason": explanation
#         })

#     # Save to JSON
#     with open(output_path, "w") as f:
#         json.dump(transactions, f, indent=2)

#     print(f"✅ Saved {len(transactions)} fraud explanations to '{output_path}'")

from pathlib import Path
import pandas as pd
import json
import time
import google.generativeai as genai

def generate_fraud_explanations():
    print("🤖 Generating Gemini explanations...")

    # Paths
    base_dir = Path(__file__).resolve().parent.parent
    csv_path = base_dir / "fraud_cases_for_llm.csv"
    history_path = base_dir / "denormalized_transactions/account_history.csv"
    output_path = base_dir / "fraud_explanations_full.json"

    # Load data
    fraud_cases = pd.read_csv(csv_path)
    account_history = pd.read_csv(history_path)

    # Ensure required columns
    if "account_id" not in fraud_cases.columns or "account_id" not in account_history.columns:
        raise ValueError("Missing 'account_id' column in one of the inputs.")

    # Normalize scores
    min_score = fraud_cases["anomaly_score"].min()
    max_score = fraud_cases["anomaly_score"].max()
    fraud_cases["score"] = (fraud_cases["anomaly_score"] - min_score) / (max_score - min_score)

    # Sort by score and keep top unique accounts
    fraud_cases_sorted = fraud_cases.sort_values(by="score", ascending=False)
    top_unique_accounts = fraud_cases_sorted.drop_duplicates(subset="account_id").head(3)

    # Merge with account history
    merged = top_unique_accounts.merge(account_history, on="account_id", how="left", suffixes=('', '_history'))

    # Configure Gemini client
    genai.configure(api_key="your_api_key_here")  # Replace with actual API key
    model = genai.GenerativeModel("gemini-1.5-pro")

    def get_explanation(row):
        transaction_info = row.drop(labels=[col for col in row.index if col.endswith('_history') or col == "score"]).to_dict()
        history_info = {k: v for k, v in row.to_dict().items() if k.endswith('_history')}

        prompt = f"""
You are an AI fraud analyst. A fraud detection model flagged the following transaction as fraud.

--- Transaction Info ---
{transaction_info}

--- Account History Info ---
{history_info}

From the details above, choose ONE concise reason (in the same intent and style) from examples like below. The reason should clearly reflect the potential fraud pattern detected. Only return the matching reason, nothing else.

Examples:
· Closing balance < ₹1000: A low remaining balance may suggest account draining, especially when followed by large debits.

· Blacklisted merchant: Transactions involving merchants previously known for suspicious activity or confirmed frauds are flagged.

· Blacklisted location: Geographical locations identified as fraud-prone or part of ongoing fraudulent rings are treated as high-risk.

· High transaction amount (>95th percentile): An unusually large amount, compared to typical customer behavior, can indicate outliers or unauthorized access.

· Foreign transaction from high-risk country: Cross-border transactions, especially from countries with known fraud associations, are treated with increased scrutiny.

· High-value withdrawal/payment on credit account: Such transactions are unexpected and may imply misuse or theft, particularly if not consistent with historical patterns.
"""
        response = model.generate_content(prompt)
        return response.text.strip()

    # Generate explanations
    transactions = []

    for idx, row in merged.iterrows():
        try:
            explanation = get_explanation(row)
        except Exception as e:
            explanation = f"Error: {e}"

        print(f"\n📝 Explanation for transaction {row.get('transaction_id', f'T{idx}')}: {explanation}\n")

        transactions.append({
            "id": row.get("transaction_id", f"T{idx}"),
            "timestamp": row.get("timestamp"),
            "amount": row.get("amount"),
            "accountNumber": row.get("account_number"),
            "transactionType": row.get("transaction_type"),
            "score": float(row["score"]),
            "reason": explanation
        })

    # Save to JSON
    with open(output_path, "w") as f:
        json.dump(transactions, f, indent=2)

    print(f"✅ Saved {len(transactions)} fraud explanations to '{output_path}'")
