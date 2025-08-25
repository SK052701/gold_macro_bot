from src.fetchers.gold_price import get_gold_price
from src.fetchers.cpi_forecast import get_latest_cpi_forecast
from src.fetchers.econ_data import get_latest_cpi_from_processed_csv
from src.ai_engine.deepseek_handler import analyze_event_with_deepseek
from src.fetchers.scrape_cpi_forecast import update_forecast_json



import datetime
import os

def run_analysis():

    # Update forecast data by scraping Investing.com
    update_forecast_json()

    # Get current gold price
    gold_price = get_gold_price()
    print(f"Gold Price: ${gold_price}")

    # Get CPI data
    
    cpi_actual, period_date = get_latest_cpi_from_processed_csv()
    cpi_expected, release_date = get_latest_cpi_forecast()

    print(f"CPI Actual: {cpi_actual}% | Expected: {cpi_expected}%")

    # Run GPT analysis
    sentiment = analyze_event_with_deepseek(cpi_actual, cpi_expected, gold_price)
    print(f"DeepSeek Sentiment: {sentiment}")

    # Log the result
    log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = (
    f"\n{'='*80}\n"
    f"{log_time} | Gold: ${gold_price} | CPI: {cpi_actual}/{cpi_expected} | Sentiment: {sentiment}\n"
)


    os.makedirs("logs", exist_ok=True)
    with open("logs/signals.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

    # Return structured result for future use
    return {
        "timestamp": log_time,
        "gold_price": gold_price,
        "cpi_actual": cpi_actual,
        "cpi_expected": cpi_expected,
        "sentiment": sentiment
    }

if __name__ == "__main__":
    result = run_analysis()
    print("\nReturned Result:\n", result)
