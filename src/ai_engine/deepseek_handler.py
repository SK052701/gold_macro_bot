import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def analyze_event_with_deepseek(cpi_actual, cpi_expected, gold_price):
    try:
        prompt = (
            f"The latest CPI came in at {cpi_actual}% while the market expected {cpi_expected}%. "
            f"Gold is currently trading at ${gold_price}. "
            f"Based on this CPI surprise, what is the likely 2–10 day swing trading outlook for gold?"
	    f"Keep in mind the geopolitical news that have been happening for the past month"
        )

        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://github.com/SK052701",
                "X-Title": "Gold Macro Bot",                           
            },
            extra_body={},  # can stay empty
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {"role": "system", "content": "You are a macro trading analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {e}"
