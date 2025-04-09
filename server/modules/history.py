# import pandas as pd
 
# # Load denormalized transactions (cleaned)
# df = pd.read_csv("/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/non_fraud_transactions.csv")
 
# # Ensure numeric columns are properly typed
# df["amount"] = pd.to_numeric(df["amount"], errors='coerce')
# df["opening_balance"] = pd.to_numeric(df["opening_balance"], errors='coerce')
# df["closing_balance"] = pd.to_numeric(df["closing_balance"], errors='coerce')
# df["is_fraud"] = df["is_fraud"].astype(bool)
 
# # Create account-level history by grouping
# account_history = df.groupby("account_id").agg({
#     "transaction_id": "count",  # Total transactions
#     "amount": ["mean", "std", "max", "min", "sum"],
#     "opening_balance": "mean",
#     "closing_balance": ["mean", "max"],
#     "is_fraud": "sum",  # Total frauds
#     "transaction_type": pd.Series.nunique,
#     "merchant": pd.Series.nunique,
#     "location": pd.Series.nunique
# })
 
# # Flatten multi-level columns
# account_history.columns = ['_'.join(col).strip() for col in account_history.columns.values]
 
# # Reset index
# account_history.reset_index(inplace=True)
 
# # Optional: rename columns for clarity
# account_history.rename(columns={
#     "transaction_id_count": "num_transactions",
#     "amount_mean": "avg_amount",
#     "amount_std": "std_amount",
#     "amount_max": "max_amount",
#     "amount_min": "min_amount",
#     "amount_sum": "total_amount",
#     "opening_balance_mean": "avg_opening_balance",
#     "closing_balance_mean": "avg_closing_balance",
#     "closing_balance_max": "max_closing_balance",
#     "is_fraud_sum": "num_frauds",
#     "transaction_type_nunique": "unique_transaction_types",
#     "merchant_nunique": "unique_merchants",
#     "location_nunique": "unique_locations"
# }, inplace=True)
 
# # Save to CSV
# account_history.to_csv("account_history.csv", index=False)
# print("✅ Account-level transaction history saved to 'account_history.csv'")
 


# import pandas as pd
# import os


# def generate_account_level_history(input_csv: str, output_csv: str = "account_history.csv"):
#     print("📚 Generating account-level transaction history...")

#     df = pd.read_csv(input_csv)

#     # Ensure numeric columns are properly typed
#     df["amount"] = pd.to_numeric(df["amount"], errors='coerce')
#     df["opening_balance"] = pd.to_numeric(df["opening_balance"], errors='coerce')
#     df["closing_balance"] = pd.to_numeric(df["closing_balance"], errors='coerce')

#     if "is_fraud" in df.columns:
#         df["is_fraud"] = df["is_fraud"].astype(bool)
#     else:
#         df["is_fraud"] = False

#     # Group by account_id
#     account_history = df.groupby("account_id").agg({
#         "transaction_id": "count",
#         "amount": ["mean", "std", "max", "min", "sum"],
#         "opening_balance": "mean",
#         "closing_balance": ["mean", "max"],
#         "is_fraud": "sum",
#         "transaction_type": pd.Series.nunique,
#         "merchant": pd.Series.nunique,
#         "location": pd.Series.nunique
#     })

#     # Flatten multi-index columns
#     account_history.columns = ['_'.join(col).strip() for col in account_history.columns.values]
#     account_history.reset_index(inplace=True)

#     # Rename for clarity
#     account_history.rename(columns={
#         "transaction_id_count": "num_transactions",
#         "amount_mean": "avg_amount",
#         "amount_std": "std_amount",
#         "amount_max": "max_amount",
#         "amount_min": "min_amount",
#         "amount_sum": "total_amount",
#         "opening_balance_mean": "avg_opening_balance",
#         "closing_balance_mean": "avg_closing_balance",
#         "closing_balance_max": "max_closing_balance",
#         "is_fraud_sum": "num_frauds",
#         "transaction_type_nunique": "unique_transaction_types",
#         "merchant_nunique": "unique_merchants",
#         "location_nunique": "unique_locations"
#     }, inplace=True)

#     output_path = os.path.join(os.path.dirname(input_csv), output_csv)
#     account_history.to_csv(output_path, index=False)

#     print(f"✅ Account-level transaction history saved to '{output_path}'")
#     return output_path



import pandas as pd
import os

def generate_account_level_history(input_dir: str, output_csv: str = "account_history.csv"):
    print("📚 Generating account-level transaction history...")

    # Find the Spark-style output CSV
    part_file = next((f for f in os.listdir(input_dir) if f.startswith("part-") and f.endswith(".csv")), None)
    if not part_file:
        raise FileNotFoundError("❌ No part-*.csv file found in directory.")

    input_csv = os.path.join(input_dir, part_file)
    df = pd.read_csv(input_csv)

    # Ensure numeric columns are properly typed
    df["amount"] = pd.to_numeric(df["amount"], errors='coerce')
    df["opening_balance"] = pd.to_numeric(df["opening_balance"], errors='coerce')
    df["closing_balance"] = pd.to_numeric(df["closing_balance"], errors='coerce')

    if "is_fraud" in df.columns:
        df["is_fraud"] = df["is_fraud"].astype(bool)
    else:
        df["is_fraud"] = False

    # Group by account_id
    account_history = df.groupby("account_id").agg({
        "transaction_id": "count",
        "amount": ["mean", "std", "max", "min", "sum"],
        "opening_balance": "mean",
        "closing_balance": ["mean", "max"],
        "is_fraud": "sum",
        "transaction_type": pd.Series.nunique,
        "merchant": pd.Series.nunique,
        "location": pd.Series.nunique
    })

    # Flatten multi-index columns
    account_history.columns = ['_'.join(col).strip() for col in account_history.columns.values]
    account_history.reset_index(inplace=True)

    # Rename for clarity
    account_history.rename(columns={
        "transaction_id_count": "num_transactions",
        "amount_mean": "avg_amount",
        "amount_std": "std_amount",
        "amount_max": "max_amount",
        "amount_min": "min_amount",
        "amount_sum": "total_amount",
        "opening_balance_mean": "avg_opening_balance",
        "closing_balance_mean": "avg_closing_balance",
        "closing_balance_max": "max_closing_balance",
        "is_fraud_sum": "num_frauds",
        "transaction_type_nunique": "unique_transaction_types",
        "merchant_nunique": "unique_merchants",
        "location_nunique": "unique_locations"
    }, inplace=True)

    output_path = os.path.join(input_dir, output_csv)
    account_history.to_csv(output_path, index=False)

    print(f"✅ Account-level transaction history saved to '{output_path}'")
    return output_path
