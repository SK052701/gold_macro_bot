from dotenv import load_dotenv
import os
import openai

# Load API key from .env file
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# List all available models for your account
models = client.models.list()
for model in models.data:
    print(model.id)
