import requests
from bs4 import BeautifulSoup
import json
import datetime
import os

def update_forecast_json():
    url = "https://www.investing.com/economic-calendar/"
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to load Investing.com calendar")
        return

    soup = BeautifulSoup(response.text, "lxml")
    events = soup.select("tr.js-event-item")

    new_forecasts = {}

    for event in events:
        title = event.get("data-event-title", "")
        country = event.get("data-country", "")
        if "CPI" in title and "YoY" in title and country == "United States":
            date_str = event.get("data-event-datetime", "")
            forecast_str = event.get("data-forecast", "")
            if forecast_str and date_str:
                try:
                    forecast_val = float(forecast_str.strip('%'))
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    date_key = date_obj.strftime("%Y-%m-%d")
                    new_forecasts[date_key] = forecast_val
                except Exception as e:
                    print(f"⚠️ Error parsing forecast: {e}")

    forecast_path = "data/raw/cpi_forecasts.json"

    # 👇 Append to existing file if it exists
    if os.path.exists(forecast_path):
        with open(forecast_path, "r") as f:
            existing_forecasts = json.load(f)
    else:
        existing_forecasts = {}

    # 📌 Merge new forecasts (new values replace same-date ones)
    for date_key, forecast_val in new_forecasts.items():
        existing_forecasts[date_key] = forecast_val

    # 💾 Save updated forecasts
    os.makedirs("data/raw", exist_ok=True)
    with open(forecast_path, "w") as f:
        json.dump(existing_forecasts, f, indent=2)

    print(f"✅ Appended {len(new_forecasts)} new forecasts (total: {len(existing_forecasts)})")

if __name__ == "__main__":
    scrape_cpi_forecast()
