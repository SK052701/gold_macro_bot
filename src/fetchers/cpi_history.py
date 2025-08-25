import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")
SERIES_ID = "CPIAUCSL"

def fetch_cpi_fred():
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={SERIES_ID}&api_key={API_KEY}&file_type=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()["observations"]
        df = pd.DataFrame(data)[["date", "value"]]
        df.rename(columns={"value": "cpi"}, inplace=True)
        df.to_csv("data/raw/cpi_history.csv", index=False)
        print("✅ CPI data saved to data/raw/cpi_history.csv")
        print(df.tail())
        return df
    else:
        print("❌ Failed to fetch data:", response.status_code, response.text)

if __name__ == "__main__":
    fetch_cpi_fred()
