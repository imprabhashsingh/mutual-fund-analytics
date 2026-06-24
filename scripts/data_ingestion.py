import pandas as pd
import os

data_path = "data/raw"

for file in os.listdir(data_path):
    if file.endswith(".csv"):
        print("\n" + "=" * 60)
        print("FILE:", file)

        df = pd.read_csv(os.path.join(data_path, file))

        print("Shape:", df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())