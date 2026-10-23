import os
from typing import Any, Dict, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def translate_invoice_note(note: str, target_language: str = "en", source_language: Optional[str] = None, api_key: Optional[str] = None) -> str:
    if not note:
        return ""

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    system_message = "You translate invoice notes and descriptions accurately and concisely. Return only the translated text."
    user_message = f"Translate the following invoice note into {target_language}."
    if source_language:
        user_message += f" The source language is {source_language}."
    user_message += f"\n\n{note}"

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    choices = data.get("choices") or []
    if not choices:
        raise ValueError("No translation returned by OpenAI")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        raise ValueError("Unexpected OpenAI response format")
    return content.strip()
