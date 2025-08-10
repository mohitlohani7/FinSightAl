# FinSight AI

FinSight AI is a Streamlit-based transaction analysis tool that performs EDA, anomaly detection and generates AI-driven insights using the Groq LLM API. It's platform-agnostic — upload CSVs exported from PayPal, Stripe, your bank, or crypto exchanges.

## Quickstart
1. Clone the folder into VS Code.
2. Create a virtualenv and install requirements: `pip install -r requirements.txt`.
3. Set your Groq API key in environment: `export GROQ_API_KEY=your_key` (Linux/macOS) or set in config/settings.py for testing.
4. Run: `streamlit run app.py`
