import pandas as pd

fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")

fund_codes = set(fund_master["amfi_code"])
nav_codes = set(nav_history["amfi_code"])

missing_codes = fund_codes - nav_codes

print("Total AMFI Codes in Fund Master:", len(fund_codes))
print("Total AMFI Codes in NAV History:", len(nav_codes))
print("Missing Codes:", len(missing_codes))

if len(missing_codes) == 0:
    print("\nAll AMFI Codes Validated Successfully")
else:
    print("\nMissing AMFI Codes:")
    print(missing_codes)