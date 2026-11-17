
import os
from dotenv import load_dotenv

# Load the root project .env file
load_dotenv("../.env")

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("API key found!")
    print("Key length:", len(api_key))
    print("Key starts with:", api_key[:5])
else:
    print("ERROR: API key not found!")
