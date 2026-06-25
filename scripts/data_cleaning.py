import pandas as pd
import os

raw_path = "data/raw"
processed_path = "data/processed"

os.makedirs(processed_path, exist_ok=True)

# =====================================
# 1. Clean NAV History
# =====================================

nav = pd.read_csv(f"{raw_path}/02_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"])

nav = nav.sort_values(["amfi_code", "date"])

nav["nav"] = nav.groupby("amfi_code")["nav"].ffill()

nav = nav.drop_duplicates()

nav = nav[nav["nav"] > 0]

nav.to_csv(f"{processed_path}/02_nav_history.csv", index=False)

print(" NAV History Cleaned")


# =====================================
# 2. Clean Investor Transactions
# =====================================

txn = pd.read_csv(f"{raw_path}/08_investor_transactions.csv")

# Date conversion
txn["transaction_date"] = pd.to_datetime(txn["transaction_date"])

# Standardize transaction types
txn["transaction_type"] = txn["transaction_type"].str.strip().str.upper()

txn["transaction_type"] = txn["transaction_type"].replace({
    "SIP": "SIP",
    "LUMPSUM": "Lumpsum",
    "REDEMPTION": "Redemption"
})

# Remove invalid amounts
txn = txn[txn["amount_inr"] > 0]

# Remove duplicate rows
txn = txn.drop_duplicates()

# Check KYC values
valid_kyc = ["Verified", "Pending", "Rejected"]

txn["kyc_status"] = txn["kyc_status"].astype(str).str.strip()

invalid_kyc = txn[~txn["kyc_status"].isin(valid_kyc)]

if len(invalid_kyc) > 0:
    print("\n⚠ Invalid KYC Values Found")
    print(invalid_kyc["kyc_status"].unique())

txn.to_csv(
    f"{processed_path}/08_investor_transactions.csv",
    index=False
)

print(" Investor Transactions Cleaned")


# =====================================
# 3. Clean Scheme Performance
# =====================================

perf = pd.read_csv(f"{raw_path}/07_scheme_performance.csv")

return_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct"
]

for col in return_columns:
    perf[col] = pd.to_numeric(perf[col], errors="coerce")

perf = perf.drop_duplicates()

perf = perf[
    (perf["expense_ratio_pct"] >= 0.1)
    &
    (perf["expense_ratio_pct"] <= 2.5)
]

perf.to_csv(
    f"{processed_path}/07_scheme_performance.csv",
    index=False
)

print(" Scheme Performance Cleaned")

print("\n All Datasets Cleaned Successfully.")