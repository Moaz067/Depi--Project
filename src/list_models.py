from google.genai import Client
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
client = Client(api_key=os.getenv("GEMINI_API_KEY"))

# List all available models
for m in client.models.list():
    print(m.name, m.supported_actions)
