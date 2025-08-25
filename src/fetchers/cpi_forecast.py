import os
import json
from datetime import datetime

def get_latest_cpi_forecast():
    forecast_path = "data/raw/cpi_forecasts.json"

    if not os.path.exists(forecast_path):
        print("⚠️ Forecast file not found. Using fallback.")
        return None, None

    with open(forecast_path, "r") as f:
        forecasts = json.load(f)

    if not forecasts:
        print("⚠️ Forecast file is empty.")
        return None, None

    # Get the latest forecast by date
    latest_date = max(forecasts.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d"))
    return forecasts[latest_date], latest_date

