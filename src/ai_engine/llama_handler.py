import os
import requests
from dotenv import load_dotenv

load_dotenv()

def analyze_event_with_llama(cpi_actual, cpi_expected, gold_price):
    api_key = os.getenv("OPENROUTER_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/sergeykurbakov",  # Replace with your actual referer if different
        "Content-Type": "application/json"
    }

    prompt = (
        f"The latest CPI came in at {cpi_actual}% while the market expected {cpi_expected}%. "
        f"Gold is currently trading at ${gold_price}. "
        f"Based on this CPI surprise, what is the likely 2–10 day swing trading outlook for gold?"
    )

    data = {
        "model": "meta-llama/llama-2-70b-chat",
        "messages": [
            {"role": "system", "content": "You are a macro trading analyst."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = response.json()
        
        # Debug: Print raw response (optional)
        # print("LLaMA raw response:", result)

        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"Error: Invalid response structure: {result}"

    except Exception as e:
        return f"Error: {e}"
