import os
from typing import Optional

import requests


OPENAI_TRANSLATE_MODEL = "gpt-4o-mini"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def translate_consent_copy(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    messages = [
        {
            "role": "system",
            "content": "Translate identity-provider consent copy accurately, preserving meaning, product names, and legal nuance.",
        },
        {
            "role": "user",
            "content": _build_prompt(text=text, target_language=target_language, source_language=source_language),
        },
    ]

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_TRANSLATE_MODEL,
            "messages": messages,
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"].strip()


def _build_prompt(text: str, target_language: str, source_language: Optional[str]) -> str:
    parts = [f"Translate the following consent copy into {target_language}."]
    if source_language:
        parts.append(f"The source language is {source_language}.")
    parts.append("Return only the translated text.")
    parts.append("")
    parts.append(text)
    return "\n".join(parts)
