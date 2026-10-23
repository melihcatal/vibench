import os

import requests


OPENAI_TRANSLATE_MODEL = os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4.1-mini")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def alt_text_translate(text, target_language):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_TRANSLATE_MODEL,
            "messages": [
                {"role": "system", "content": "Translate image descriptions accurately and concisely."},
                {"role": "user", "content": f"Translate this into {target_language}: {text}"},
            ],
            "temperature": 0.1,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
