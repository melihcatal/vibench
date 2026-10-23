import os
from typing import Optional

import requests


def translate_text(text: str, source_language: str, target_language: str, api_key: Optional[str] = None, model: str = "gpt-4o-mini") -> str:
    if not text:
        return ""
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": f"Translate from {source_language} to {target_language}. Return only the translated text.",
                },
                {"role": "user", "content": text},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
