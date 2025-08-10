import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama3-70b-8192")

APP_TITLE = "FinSight AI"
APP_DESCRIPTION = "AI-powered transaction analysis & fraud insights"

if not GROQ_API_KEY:
    print("⚠️ Warning: GROQ_API_KEY is not set. AI features may not work.")
