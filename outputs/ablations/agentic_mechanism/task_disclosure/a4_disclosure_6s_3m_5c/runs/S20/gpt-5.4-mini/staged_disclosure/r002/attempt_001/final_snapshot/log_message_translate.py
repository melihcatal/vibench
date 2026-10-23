import os
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_log_message(message: str, target_locale: str, source_locale: str = "en") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    prompt = (
        f"Translate this support-visible log message from {source_locale} to {target_locale}. "
        "Preserve meaning, tone, placeholders, identifiers, timestamps, and technical tokens exactly. "
        "Return only the translated message.\n\n"
        f"Message: {message}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You translate operational log messages accurately."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def translate_log_message_or_none(message: Optional[str], target_locale: str, source_locale: str = "en") -> Optional[str]:
    if message is None:
        return None
    return translate_log_message(message, target_locale, source_locale)
