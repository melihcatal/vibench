import os
import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def check_live_transcript_safety(transcript: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You evaluate live transcript text for unsafe content and return JSON with keys safe, risk_categories, and reason.",
            },
            {"role": "user", "content": transcript},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    return __import__("json").loads(content)
