import pandas as pd

def get_latest_cpi_from_processed_csv():

    # Load processed CPI data
    df = pd.read_csv("data/processed/cpi_processed.csv")
    df["date"] = pd.to_datetime(df["date"])

    # Get the most recent row
    latest = df.sort_values("date").iloc[-1]

    # Actual YoY CPI
    actual_cpi_yoy = round(latest["cpi_yoy"], 2)

  

    return actual_cpi_yoy, latest["date"].strftime("%Y-%m-%d")
