import os
from typing import Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _get_locale() -> str:
    return os.getenv("USER_LOCALE", os.getenv("LANG", "en")).split(".")[0].replace("_", "-")


def translate_onboarding_copy(copy: str, locale: Optional[str] = None) -> str:
    target_locale = locale or _get_locale()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Translate onboarding copy into the target locale. Return only the translation."},
                {"role": "user", "content": f"Locale: {target_locale}\nCopy: {copy}"},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
