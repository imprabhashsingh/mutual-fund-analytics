import pandas as pd

df = pd.read_csv("data/raw/01_fund_master.csv")

print("\nUnique Fund Houses:")
print(df["fund_house"].unique())

print("\nNumber of Fund Houses:")
print(df["fund_house"].nunique())

print("\nCategories:")
print(df["category"].unique())

print("\nSub Categories:")
print(df["sub_category"].unique())

if "risk_grade" in df.columns:
    print("\nRisk Grades:")
    print(df["risk_grade"].unique())
else:
    print("\nNo risk_grade column found")