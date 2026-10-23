import os
from typing import Optional

import httpx


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_live_captions(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    if not text.strip():
        return ""

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_prompt = "Translate live captions faithfully, preserving meaning, names, numbers, and punctuation. Return only the translated text."
    if source_language:
        user_prompt = f"Translate from {source_language} to {target_language}: {text}"
    else:
        user_prompt = f"Translate to {target_language}: {text}"

    response = httpx.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        },
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
