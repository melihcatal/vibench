import os

import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def translate_consent_copy(text: str, target_language: str) -> str:
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={
            "model": "gpt-4.1-mini",
            "messages": [
                {"role": "user", "content": f"Translate to {target_language}: {text}"}
            ],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
