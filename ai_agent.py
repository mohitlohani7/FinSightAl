import os
import json
import requests
from typing import Optional
from config.settings import GROQ_API_KEY, GROQ_MODEL

def call_groq_chat(system_prompt: str, user_prompt: str, top_k: int = 1) -> Optional[str]:
    api_key = os.environ.get("GROQ_API_KEY", GROQ_API_KEY)
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Put it in environment or config/settings.py")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.2
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code != 200:
        return f"Groq API error {resp.status_code}: {resp.text}"

    j = resp.json()
    try:
        content = j["choices"][0]["message"]["content"]
        return content
    except Exception:
        return json.dumps(j, indent=2)

def dataset_summary_prompt(df_head_csv: str) -> str:
    return (
        "You are a data analyst specialized in fintech transactions. "
        "Given the following CSV snippet (first rows) and column names, produce a concise bullet-list of: \n"
        "1) top suspicious patterns to investigate, 2) three suggested anomaly detection checks, 3) a one-paragraph summary of spending trends.\n\n"
        f"Data:\n{df_head_csv}\n\nReturn plain text bullets."
    )

def generate_insights_from_df(df):
    head_csv = df.head(50).to_csv(index=False)
    system = "You are FinSight AI assistant. Be concise and actionable."
    prompt = dataset_summary_prompt(head_csv)
    return call_groq_chat(system, prompt)

# New function to allow question-answering interaction
def generate_insights_from_df_with_question(df, question: str):
    head_csv = df.head(50).to_csv(index=False)
    system = "You are FinSight AI assistant. Be concise and actionable."
    prompt = (
        f"Given the following CSV data snippet:\n{head_csv}\n"
        f"Answer this question:\n{question}\n"
        "Provide clear and concise response."
    )
    return call_groq_chat(system, prompt)
