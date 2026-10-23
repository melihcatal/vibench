import os

import requests


OPENAI_SAFETY_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4.1-mini")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def visual_safety_text(labels):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_SAFETY_MODEL,
            "messages": [
                {"role": "system", "content": "Assess whether visual labels contain unsafe text."},
                {"role": "user", "content": str(labels)},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
