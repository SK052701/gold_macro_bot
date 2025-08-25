import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # NEW SYNTAX

def analyze_event_with_gpt(cpi_actual, cpi_expected, gold_price):
    prompt = (
        f"The latest CPI came in at {cpi_actual}% while the market expected {cpi_expected}%. "
        f"Gold is currently trading at ${gold_price}. "
        f"Based on this CPI surprise, what is the likely swing trading (2–10 days) outlook for gold: bullish, bearish, or neutral? "
        f"Briefly explain why."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a macro trading analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"