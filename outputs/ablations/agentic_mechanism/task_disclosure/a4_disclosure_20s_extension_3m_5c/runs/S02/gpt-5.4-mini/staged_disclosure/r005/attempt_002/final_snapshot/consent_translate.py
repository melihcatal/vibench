import os
from typing import Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_consent_copy(text: str, target_language: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    payload: Dict[str, object] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "Translate identity-provider consent copy accurately and naturally."},
            {"role": "user", "content": f"Translate the following consent text into {target_language}: {text}"},
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
