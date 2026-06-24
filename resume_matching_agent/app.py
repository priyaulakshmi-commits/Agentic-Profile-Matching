from dotenv import load_dotenv
import os

load_dotenv()

print("API Key Loaded:", os.getenv("GROQ_API_KEY") is not None)