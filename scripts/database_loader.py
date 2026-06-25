import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import os

# ==========================================
# Paths
# ==========================================

DB_PATH = "bluestock_mf.db"
SCHEMA_PATH = "sql/schema.sql"
PROCESSED_PATH = "data/processed"

# ==========================================
# Create SQLite Database
# ==========================================

engine = create_engine(f"sqlite:///{DB_PATH}")
print("Database created successfully.")

# ==========================================
# Execute Schema
# ==========================================

conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, "r") as file:
    schema = file.read()

conn.executescript(schema)

print("Schema Executed Successfully")

conn.close()

# ==========================================
# Load Dimension Table : dim_fund
# ==========================================

fund = pd.read_csv("data/raw/01_fund_master.csv")

print("\nFund Master Columns:")
print(fund.columns.tolist())

# ==========================================
# Load dim_fund
# ==========================================

fund = fund[
    [
        "amfi_code",
        "scheme_name",
        "fund_house",
        "category",
        "sub_category",
        "plan",
        "benchmark",
        "fund_manager",
        "expense_ratio_pct",
        "exit_load_pct",
        "min_sip_amount",
        "min_lumpsum_amount",
        "risk_category",
        "sebi_category_code"
    ]
]

fund.to_sql(
    "dim_fund",
    engine,
    if_exists="append",
    index=False
)

print(f"\n dim_fund Loaded Successfully ({len(fund)} records)")

# ==========================================
# Load Dimension Table : dim_date
# ==========================================

print("\nCreating Date Dimension...")

# ==========================================
# Create Complete Calendar Date Dimension
# ==========================================

dates = pd.DataFrame({
    "full_date": pd.date_range(
        start="2022-01-01",
        end="2026-12-31",
        freq="D"
    )
})
dates["day"] = dates["full_date"].dt.day
dates["month"] = dates["full_date"].dt.month
dates["month_name"] = dates["full_date"].dt.month_name()
dates["quarter"] = dates["full_date"].dt.quarter
dates["year"] = dates["full_date"].dt.year
dates["weekday"] = dates["full_date"].dt.day_name()

# Insert into database
dates.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False
)

print(f" dim_date Loaded Successfully ({len(dates)} records)")

# ==========================================
# Load Fact Table : fact_nav
# ==========================================

print("\nLoading fact_nav...")
nav = pd.read_csv(f"{PROCESSED_PATH}/02_nav_history.csv")

fund_dim = pd.read_sql("SELECT fund_id, amfi_code FROM dim_fund", engine)

date_dim = pd.read_sql("SELECT date_id, full_date FROM dim_date", engine)
nav = nav.merge(fund_dim, on="amfi_code")

date_dim["full_date"] = pd.to_datetime(date_dim["full_date"])

nav["date"] = pd.to_datetime(nav["date"])

nav = nav.merge(
    date_dim,
    left_on="date",
    right_on="full_date"
)
nav = nav[
    [
        "fund_id",
        "date_id",
        "nav"
    ]
]
nav.to_sql(
    "fact_nav",
    engine,
    if_exists="append",
    index=False
)

print(f"fact_nav loaded successfully. Records: {len(nav)}")

# ==========================================
# Load Fact Table : fact_transactions
# ==========================================

print("\nLoading fact_transactions...")

txn = pd.read_csv(f"{PROCESSED_PATH}/08_investor_transactions.csv")

# Read fund dimension
fund_dim = pd.read_sql(
    "SELECT fund_id, amfi_code FROM dim_fund",
    engine
)
txn = txn.merge(
    fund_dim,
    on="amfi_code"
)

# Convert transaction date to datetime
txn["transaction_date"] = pd.to_datetime(txn["transaction_date"])
txn_dates = set(txn["transaction_date"])

date_dim_dates = set(date_dim["full_date"])

missing_dates = txn_dates - date_dim_dates
print("Transaction Date Converted")

# Read date dimension
date_dim = pd.read_sql(
    "SELECT date_id, full_date FROM dim_date",
    engine
)

# Convert full_date to datetime
date_dim["full_date"] = pd.to_datetime(date_dim["full_date"])

# Map transaction_date -> date_id
txn = txn.merge(
    date_dim,
    left_on="transaction_date",
    right_on="full_date"
)

print("Date Mapping Completed")
print(f"fact_transactions loaded successfully. Records: {len(txn)}")

# ==========================================
# Load Fact Table : fact_performance
# ==========================================

print("\nLoading fact_performance...")

perf = pd.read_csv(f"{PROCESSED_PATH}/07_scheme_performance.csv")

# Read fund dimension
fund_dim = pd.read_sql(
    "SELECT fund_id, amfi_code FROM dim_fund",
    engine
)

# Map amfi_code -> fund_id
perf = perf.merge(
    fund_dim,
    on="amfi_code"
)

print("Fund Mapping Completed")
print(f"Rows after fund mapping: {len(perf)}")

# Select required columns
perf = perf[
    [
        "fund_id",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "expense_ratio_pct",
        "morningstar_rating",
        "risk_grade"
    ]
]

print("Columns Selected Successfully")
print(f"Columns: {list(perf.columns)}")

# Load into fact_performance
perf.to_sql(
    "fact_performance",
    engine,
    if_exists="append",
    index=False
)

print(f"fact_performance loaded successfully. Records: {len(perf)}")

# ==========================================
# Load Fact Table : fact_aum
# ==========================================

print("\nLoading fact_aum...")

aum = pd.read_csv(f"{PROCESSED_PATH}/07_scheme_performance.csv")

# Read fund dimension
fund_dim = pd.read_sql(
    "SELECT fund_id, amfi_code FROM dim_fund",
    engine
)
# Map amfi_code -> fund_id
aum = aum.merge(
    fund_dim,
    on="amfi_code"
)

print("Fund Mapping Completed")
print(f"Rows after fund mapping: {len(aum)}")

# Select required columns
aum = aum[
    [
        "fund_id",
        "aum_crore"
    ]
]

print(f"Columns: {list(aum.columns)}")

# Load into fact_aum
aum.to_sql(
    "fact_aum",
    engine,
    if_exists="append",
    index=False
)

print(f"fact_aum loaded successfully. Records: {len(aum)}")