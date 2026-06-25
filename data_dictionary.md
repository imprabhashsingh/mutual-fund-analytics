# Mutual Fund Analytics - Data Dictionary

## dim_fund

| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| fund_id | INTEGER | Primary Key | Generated |
| amfi_code | INTEGER | AMFI Scheme Code | fund_master.csv |
| scheme_name | TEXT | Mutual Fund Scheme Name | fund_master.csv |
| fund_house | TEXT | Fund House Name | fund_master.csv |
| category | TEXT | Fund Category | fund_master.csv |
| sub_category | TEXT | Sub Category | fund_master.csv |
| risk_grade | TEXT | Risk Rating | fund_master.csv |

---

## dim_date

| Column | Data Type | Description |
|--------|-----------|-------------|
| date_id | INTEGER | Primary Key |
| full_date | DATE | Calendar Date |
| day | INTEGER | Day |
| month | INTEGER | Month |
| month_name | TEXT | Month Name |
| quarter | INTEGER | Quarter |
| year | INTEGER | Year |

---

## fact_nav

| Column | Data Type | Description |
|--------|-----------|-------------|
| nav_id | INTEGER | Primary Key |
| fund_id | INTEGER | Foreign Key |
| date_id | INTEGER | Foreign Key |
| nav | REAL | Net Asset Value |

---

## fact_transactions

| Column | Data Type | Description |
|--------|-----------|-------------|
| transaction_id | INTEGER | Primary Key |
| fund_id | INTEGER | Foreign Key |
| date_id | INTEGER | Foreign Key |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount | REAL | Investment Amount |
| investor_state | TEXT | Investor State |
| kyc_status | TEXT | KYC Status |

---

## fact_performance

| Column | Data Type | Description |
|--------|-----------|-------------|
| performance_id | INTEGER | Primary Key |
| fund_id | INTEGER | Foreign Key |
| return_1yr_pct | REAL | 1 Year Return |
| return_3yr_pct | REAL | 3 Year Return |
| return_5yr_pct | REAL | 5 Year Return |
| expense_ratio | REAL | Expense Ratio |

---

## fact_aum

| Column | Data Type | Description |
|--------|-----------|-------------|
| aum_id | INTEGER | Primary Key |
| fund_id | INTEGER | Foreign Key |
| aum_crore | REAL | Assets Under Management (Crores) |