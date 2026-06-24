import requests
import pandas as pd
import os

scheme_codes = {
    "HDFC_Top_100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

output_folder = "data/raw/live_nav"
os.makedirs(output_folder, exist_ok=True)

for name, code in scheme_codes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        nav_df = pd.DataFrame(data["data"])

        nav_df.to_csv(
            f"{output_folder}/{name}.csv",
            index=False
        )

        print(f"Saved: {name}")

    else:
        print(f"Failed: {name}")