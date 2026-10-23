import os
from typing import Iterable, List

import requests

OPENAI_TRANSLATION_MODEL = "gpt-5.4-mini"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def translate_consent_copy(text: str, target_language: str, source_language: str = "en") -> str:
    api_key = os.environ["OPENAI_API_KEY"]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    prompt = (
        f"Translate the following identity-provider consent copy from {source_language} to {target_language}. "
        "Preserve meaning, tone, placeholders, product names, and any legal terminology. Return only the translation.

"
        f"{text}"
    )
    payload = {
        "model": OPENAI_TRANSLATION_MODEL,
        "messages": [
            {"role": "system", "content": "You are a precise translation engine for identity-provider consent screens."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def translate_consent_lines(lines: Iterable[str], target_language: str, source_language: str = "en") -> List[str]:
    return [translate_consent_copy(line, target_language, source_language) for line in lines]
