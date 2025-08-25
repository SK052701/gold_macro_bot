import pandas as pd

def process_cpi_data(filepath="data/raw/cpi_history.csv"):
    # Load CPI data
    df = pd.read_csv(filepath)

    # Ensure correct types
    df["date"] = pd.to_datetime(df["date"])
    df["cpi"] = pd.to_numeric(df["cpi"], errors="coerce")

    # Sort by date just in case
    df = df.sort_values("date").reset_index(drop=True)

    # Calculate Month-over-Month (MoM) % change
    df["cpi_mom"] = df["cpi"].pct_change() * 100

    # Calculate Year-over-Year (YoY) % change
    df["cpi_yoy"] = df["cpi"].pct_change(periods=12) * 100

    # Drop rows with NaN in new columns
    df = df.dropna(subset=["cpi_mom", "cpi_yoy"])

    # Save processed version
    df.to_csv("data/processed/cpi_processed.csv", index=False)
    print("✅ CPI data processed and saved to data/processed/cpi_processed.csv")
    print(df.tail())

    return df

if __name__ == "__main__":
    process_cpi_data()
