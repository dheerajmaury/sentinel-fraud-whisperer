# import pandas as pd
# import numpy as np
# import random

# # ----------------------------
# # Configuration & Data Loading
# # ----------------------------

# # Define lists for blacklisted merchants and locations.
# blacklisted_merchants = ['Vision Corp', 'Pinnacle Ltd', 'Omega LLC']
# blacklisted_locations = ['Lakeview', 'Springfield', 'Newport']

# # Load the denormalized transactions CSV.
# df = pd.read_csv("denoised_enriched_transactions.csv")
# print("📊 Columns in loaded CSV:", df.columns.tolist())

# # ----------------------------
# # Check for Required Columns
# # ----------------------------

# required_columns = ['transaction_id', 'timestamp', 'amount', 'transaction_type', 'closing_balance', 'merchant', 'location', 'is_foreign', 'is_high_risk_country']
# missing_required = [col for col in required_columns if col not in df.columns]

# if missing_required:
#     raise ValueError(f"❌ Missing required columns: {missing_required}")

# # ----------------------------
# # Define Detection Thresholds
# # ----------------------------

# # Define a high-amount threshold using the 95th percentile of the 'amount' field.
# high_amount_threshold = df['amount'].quantile(0.95)

# # ----------------------------
# # Apply Rule-Based Fraud Detection
# # ----------------------------

# # Rule 1: Flag low closing balance (< ₹1000)
# df['flag_low_balance'] = df['closing_balance'] < 1000

# # Rule 2: Flag transactions with a blacklisted merchant
# df['flag_blacklisted_merchant'] = df['merchant'].isin(blacklisted_merchants)

# # Rule 3: Flag transactions that occur in a blacklisted location
# df['flag_blacklisted_location'] = df['location'].isin(blacklisted_locations)

# # Rule 4: Flag high transaction amounts (above 95th percentile)
# df['flag_high_amount'] = df['amount'] > high_amount_threshold

# # Rule 5: Flag foreign transactions from high-risk countries
# df['flag_high_risk_foreign'] = (df['is_foreign'] == True) & (df['is_high_risk_country'] == True)

# # Rule 6: Flag high-value withdrawal or payment on credit accounts (amount > ₹3000)
# if 'account_type' in df.columns:
#     df['flag_credit_withdrawal'] = (
#         (df['account_type'] == 'credit') &
#         (df['transaction_type'].isin(['withdrawal', 'payment'])) &
#         (df['amount'] > 3000)
#     )
# else:
#     df['flag_credit_withdrawal'] = False
#     print("⚠️ 'account_type' column missing; skipping Rule 6.")

# # ----------------------------
# # Split Fraud vs Non-Fraud
# # ----------------------------

# flag_columns = [
#     'flag_low_balance',
#     'flag_blacklisted_merchant',
#     'flag_blacklisted_location',
#     'flag_high_amount',
#     'flag_high_risk_foreign',
#     'flag_credit_withdrawal'
# ]

# fraud_df = df[df[flag_columns].any(axis=1)].copy()
# nonfraud_df = df[~df[flag_columns].any(axis=1)].copy()

# # ----------------------------
# # Generate Fraud Reason Strings
# # ----------------------------

# def explain_reasons(row):
#     reasons = []
#     if row['flag_low_balance']:
#         reasons.append("Closing balance < ₹1000")
#     if row['flag_blacklisted_merchant']:
#         reasons.append("Blacklisted merchant")
#     if row['flag_blacklisted_location']:
#         reasons.append("Blacklisted location")
#     if row['flag_high_amount']:
#         reasons.append("High transaction amount (>95th percentile)")
#     if row['flag_high_risk_foreign']:
#         reasons.append("Foreign transaction from high-risk country")
#     if row['flag_credit_withdrawal']:
#         reasons.append("High-value withdrawal/payment on credit account")
#     return "; ".join(reasons)

# fraud_df["reason"] = fraud_df.apply(explain_reasons, axis=1)

# # ----------------------------
# # Generate Fraud Score
# # ----------------------------

# random.seed(42)
# fraud_df['score'] = fraud_df.apply(lambda x: round(random.uniform(0.7, 1.0), 2), axis=1)

# # ----------------------------
# # Prepare Output DataFrames
# # ----------------------------

# # Handle account number field
# if 'account_number' not in fraud_df.columns:
#     if 'account_id' in fraud_df.columns:
#         fraud_df.rename(columns={'account_id': 'account_number'}, inplace=True)
#     else:
#         raise ValueError("❌ Missing both 'account_number' and 'account_id' in fraud data.")

# fraud_column_mapping = {
#     'transaction_id': 'id',
#     'timestamp': 'timestamp',
#     'amount': 'amount',
#     'account_number': 'accountNumber',
#     'transaction_type': 'transactionType',
#     'score': 'score',
#     'reason': 'reason'
# }

# fraud_csv_df = fraud_df[list(fraud_column_mapping.keys())].rename(columns=fraud_column_mapping)
# fraud_csv_df.to_csv("fraud_transactions.csv", index=False)
# print(f"✅ {len(fraud_csv_df)} fraud transactions saved to 'fraud_transactions.csv'.")

# # Output clean non-fraud transactions
# nonfraud_df_clean = nonfraud_df.drop(columns=[col for col in flag_columns if col in nonfraud_df.columns])
# nonfraud_df_clean.to_csv("non_fraud_transactions.csv", index=False)
# print(f"✅ {len(nonfraud_df_clean)} non-fraud transactions saved to 'non_fraud_transactions.csv'.")



# server/modules/rules_engine.py

# import pandas as pd
# import random

# def apply_rule_based_fraud_detection(input_csv):
#     blacklisted_merchants = ['Vision Corp', 'Pinnacle Ltd', 'Omega LLC']
#     blacklisted_locations = ['Lakeview', 'Springfield', 'Newport']

#     df = pd.read_csv(input_csv)
#     print("📊 Columns in loaded CSV:", df.columns.tolist())

#     required_columns = [
#         'transaction_id', 'timestamp', 'amount', 'transaction_type',
#         'closing_balance', 'merchant', 'location', 'is_foreign', 'is_high_risk_country'
#     ]
#     missing_required = [col for col in required_columns if col not in df.columns]
#     if missing_required:
#         raise ValueError(f"❌ Missing required columns: {missing_required}")

#     high_amount_threshold = df['amount'].quantile(0.95)

#     df['flag_low_balance'] = df['closing_balance'] < 1000
#     df['flag_blacklisted_merchant'] = df['merchant'].isin(blacklisted_merchants)
#     df['flag_blacklisted_location'] = df['location'].isin(blacklisted_locations)
#     df['flag_high_amount'] = df['amount'] > high_amount_threshold
#     df['flag_high_risk_foreign'] = (df['is_foreign']) & (df['is_high_risk_country'])

#     if 'account_type' in df.columns:
#         df['flag_credit_withdrawal'] = (
#             (df['account_type'] == 'credit') &
#             (df['transaction_type'].isin(['withdrawal', 'payment'])) &
#             (df['amount'] > 3000)
#         )
#     else:
#         df['flag_credit_withdrawal'] = False
#         print("⚠️ 'account_type' column missing; skipping Rule 6.")

#     flag_columns = [
#         'flag_low_balance', 'flag_blacklisted_merchant', 'flag_blacklisted_location',
#         'flag_high_amount', 'flag_high_risk_foreign', 'flag_credit_withdrawal'
#     ]

#     fraud_df = df[df[flag_columns].any(axis=1)].copy()
#     nonfraud_df = df[~df[flag_columns].any(axis=1)].copy()

#     def explain_reasons(row):
#         reasons = []
#         if row['flag_low_balance']:
#             reasons.append("Closing balance < ₹1000")
#         if row['flag_blacklisted_merchant']:
#             reasons.append("Blacklisted merchant")
#         if row['flag_blacklisted_location']:
#             reasons.append("Blacklisted location")
#         if row['flag_high_amount']:
#             reasons.append("High transaction amount (>95th percentile)")
#         if row['flag_high_risk_foreign']:
#             reasons.append("Foreign transaction from high-risk country")
#         if row['flag_credit_withdrawal']:
#             reasons.append("High-value withdrawal/payment on credit account")
#         return "; ".join(reasons)

#     fraud_df["reason"] = fraud_df.apply(explain_reasons, axis=1)

#     random.seed(42)
#     fraud_df['score'] = fraud_df.apply(lambda x: round(random.uniform(0.7, 1.0), 2), axis=1)

#     if 'account_number' not in fraud_df.columns and 'account_id' in fraud_df.columns:
#         fraud_df.rename(columns={'account_id': 'account_number'}, inplace=True)

#     if 'account_number' not in fraud_df.columns:
#         raise ValueError("❌ Missing both 'account_number' and 'account_id' in fraud data.")

#     fraud_column_mapping = {
#         'transaction_id': 'id',
#         'timestamp': 'timestamp',
#         'amount': 'amount',
#         'account_number': 'accountNumber',
#         'transaction_type': 'transactionType',
#         'score': 'score',
#         'reason': 'reason'
#     }

#     fraud_csv_df = fraud_df[list(fraud_column_mapping.keys())].rename(columns=fraud_column_mapping)
#     fraud_csv_df.to_csv("fraud_transactions.csv", index=False)
#     print(f"✅ {len(fraud_csv_df)} fraud transactions saved to 'fraud_transactions.csv'.")

#     nonfraud_df_clean = nonfraud_df.drop(columns=[col for col in flag_columns if col in nonfraud_df.columns])
#     nonfraud_df_clean.to_csv("non_fraud_transactions.csv", index=False)
#     print(f"✅ {len(nonfraud_df_clean)} non-fraud transactions saved to 'non_fraud_transactions.csv'.")


import pandas as pd
import random

def apply_rule_based_fraud_detection(input_csv):
    blacklisted_merchants = ['Vision Corp', 'Pinnacle Ltd', 'Omega LLC']
    blacklisted_locations = ['Lakeview', 'Springfield', 'Newport']

    df = pd.read_csv(input_csv)
    print("📊 Columns in loaded CSV:", df.columns.tolist())

    required_columns = [
        'transaction_id', 'timestamp', 'amount', 'transaction_type',
        'closing_balance', 'merchant', 'location', 'is_foreign', 'is_high_risk_country'
    ]
    missing_required = [col for col in required_columns if col not in df.columns]
    if missing_required:
        raise ValueError(f"❌ Missing required columns: {missing_required}")

    high_amount_threshold = df['amount'].quantile(0.95)

    df['flag_low_balance'] = df['closing_balance'] < 1000
    df['flag_blacklisted_merchant'] = df['merchant'].isin(blacklisted_merchants)
    df['flag_blacklisted_location'] = df['location'].isin(blacklisted_locations)
    df['flag_high_amount'] = df['amount'] > high_amount_threshold
    df['flag_high_risk_foreign'] = (df['is_foreign']) & (df['is_high_risk_country'])

    if 'account_type' in df.columns:
        df['flag_credit_withdrawal'] = (
            (df['account_type'] == 'credit') &
            (df['transaction_type'].isin(['withdrawal', 'payment'])) &
            (df['amount'] > 3000)
        )
    else:
        df['flag_credit_withdrawal'] = False
        print("⚠️ 'account_type' column missing; skipping Rule 6.")

    flag_columns = [
        'flag_low_balance', 'flag_blacklisted_merchant', 'flag_blacklisted_location',
        'flag_high_amount', 'flag_high_risk_foreign', 'flag_credit_withdrawal'
    ]

    fraud_df = df[df[flag_columns].any(axis=1)].copy()
    nonfraud_df = df[~df[flag_columns].any(axis=1)].copy()

    def explain_reasons(row):
        reasons = []
        if row['flag_low_balance']:
            reasons.append("Closing balance < ₹1000")
        if row['flag_blacklisted_merchant']:
            reasons.append("Blacklisted merchant")
        if row['flag_blacklisted_location']:
            reasons.append("Blacklisted location")
        if row['flag_high_amount']:
            reasons.append("High transaction amount (>95th percentile)")
        if row['flag_high_risk_foreign']:
            reasons.append("Foreign transaction from high-risk country")
        if row['flag_credit_withdrawal']:
            reasons.append("High-value withdrawal/payment on credit account")
        return "; ".join(reasons)

    fraud_df["reason"] = fraud_df.apply(explain_reasons, axis=1)

    random.seed(42)
    fraud_df['score'] = fraud_df.apply(lambda x: round(random.uniform(0.7, 1.0), 2), axis=1)

    if 'account_number' not in fraud_df.columns and 'account_id' in fraud_df.columns:
        fraud_df.rename(columns={'account_id': 'account_number'}, inplace=True)

    if 'account_number' not in fraud_df.columns:
        raise ValueError("❌ Missing both 'account_number' and 'account_id' in fraud data.")

    fraud_column_mapping = {
        'transaction_id': 'id',
        'timestamp': 'timestamp',
        'amount': 'amount',
        'account_number': 'accountNumber',
        'transaction_type': 'transactionType',
        'score': 'score',
        'reason': 'reason'
    }

    fraud_csv_df = fraud_df[list(fraud_column_mapping.keys())].rename(columns=fraud_column_mapping)

    # Save to CSV
    fraud_csv_df.to_csv("fraud_transactions.csv", index=False)
    print(f"✅ {len(fraud_csv_df)} fraud transactions saved to 'fraud_transactions.csv'.")

    # ✅ Save to JSON
    fraud_csv_df.to_json("fraud_transactions.json", orient="records", indent=2)
    print(f"✅ {len(fraud_csv_df)} fraud transactions also saved to 'fraud_transactions.json'.")

    # Save non-fraud data
    nonfraud_df_clean = nonfraud_df.drop(columns=[col for col in flag_columns if col in nonfraud_df.columns])
    nonfraud_df_clean.to_csv("non_fraud_transactions.csv", index=False)
    print(f"✅ {len(nonfraud_df_clean)} non-fraud transactions saved to 'non_fraud_transactions.csv'.")
