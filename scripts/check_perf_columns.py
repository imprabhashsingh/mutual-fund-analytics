import pandas as pd

perf = pd.read_csv("data/raw/07_scheme_performance.csv")

print("Columns:")
print(perf.columns.tolist())