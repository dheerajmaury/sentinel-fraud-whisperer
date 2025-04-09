# import pandas as pd
# import numpy as np
# import joblib
# from tensorflow.keras.models import load_model
 
# # 1. Load data and models
# df = pd.read_csv("/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/non_fraud_transactions.csv")  # 🔄 Replace with your new transaction data
# preprocessor = joblib.load("/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/modules/fraud_preprocessor.pkl")
# autoencoder = load_model("/home/lumiq/clone-project3/sentinel-fraud-whisperer/server/modules/fraud_autoencoder_model (1)")
 
# # 2. Define features used during training
# features_used = [
#     "transaction_id", "timestamp", "amount", "transaction_type", "merchant",
#     "location", "is_foreign", "is_high_risk_country", "opening_balance",
#     "closing_balance", "account_id", "account_type_txn", "account_type_acct",
#     "account_number", "balance", "created_at_acct", "customer_id", "name",
#     "email", "phone", "address", "dob", "created_at_cust",
#     "past_txn_count", "past_avg_amount", "past_common_merchant", "past_common_location",
#     "agg_txn_count", "agg_avg_amount", "agg_std_amount", "agg_max_amount",
#     "agg_unique_merchants", "agg_unique_locations"
# ]
 
# # 3. Process input
# X = df[features_used].copy()
# X_processed = preprocessor.transform(X).toarray()
 
# # 4. Predict reconstruction
# reconstructions = autoencoder.predict(X_processed)
# mse = np.mean(np.power(X_processed - reconstructions, 2), axis=1)
 
# # 5. Use fixed threshold (from training)
# threshold = 0.001706  # 🔧 This should be your optimal F2-score threshold
# predicted_fraud = (mse > threshold).astype(int)
 
# # 6. Save full fraud-predicted rows with scores
# df["anomaly_score"] = mse
# df["predicted_fraud"] = predicted_fraud
# fraud_cases = df[df["predicted_fraud"] == 1]
 
# fraud_cases.to_csv("fraud_cases_for_llm.csv", index=False)
# print(f"✅ Saved {len(fraud_cases)} predicted frauds to 'fraud_cases_for_llm.csv'")import pandas as pd




import os
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

def run_autoencoder_fraud_detection():
    print("🤖 Running autoencoder-based fraud detection...")

    # Dynamically resolve the path to non_fraud_transactions.csv
    base_dir = Path(__file__).resolve().parent.parent  # Go to project root
    csv_path = base_dir / "non_fraud_transactions.csv"

    if not csv_path.exists():
        print(f"⚠️ Skipping autoencoder: '{csv_path}' not found.")
        return

    # 1. Load data and models
    df = pd.read_csv(csv_path)
    preprocessor = joblib.load(base_dir / "modules/fraud_preprocessor.pkl")
    autoencoder = load_model(base_dir / "modules/fraud_autoencoder_model (1)")

    # 2. Define features used during training
    features_used = [
        "transaction_id", "timestamp", "amount", "transaction_type", "merchant",
        "location", "is_foreign", "is_high_risk_country", "opening_balance",
        "closing_balance", "account_id", "account_type_txn", "account_type_acct",
        "account_number", "balance", "created_at_acct", "customer_id", "name",
        "email", "phone", "address", "dob", "created_at_cust",
        "past_txn_count", "past_avg_amount", "past_common_merchant", "past_common_location",
        "agg_txn_count", "agg_avg_amount", "agg_std_amount", "agg_max_amount",
        "agg_unique_merchants", "agg_unique_locations"
    ]

    # 3. Process input
    X = df[features_used].copy()
    X_processed = preprocessor.transform(X).toarray()

    # 4. Predict reconstruction
    reconstructions = autoencoder.predict(X_processed)
    mse = np.mean(np.power(X_processed - reconstructions, 2), axis=1)

    # 5. Use fixed threshold (from training)
    threshold = 0.001706
    predicted_fraud = (mse > threshold).astype(int)

    # 6. Save results
    df["anomaly_score"] = mse
    df["predicted_fraud"] = predicted_fraud
    fraud_cases = df[df["predicted_fraud"] == 1]

    output_path = base_dir / "fraud_cases_for_llm.csv"
    fraud_cases.to_csv(output_path, index=False)

    print(f"✅ Saved {len(fraud_cases)} predicted frauds to '{output_path}'")
