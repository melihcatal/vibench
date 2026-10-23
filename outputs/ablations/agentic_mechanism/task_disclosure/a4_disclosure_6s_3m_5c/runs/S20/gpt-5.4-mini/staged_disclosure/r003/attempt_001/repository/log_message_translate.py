import os
from typing import List

import requests


OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def translate_log_messages(messages: List[str], target_locale: str) -> List[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    payload = {
        "model": OPENAI_TRANSLATION_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You translate support-visible log messages accurately while preserving placeholders, identifiers, and formatting.",
            },
            {
                "role": "user",
                "content": f"Translate these log messages to {target_locale}. Return a JSON array of translated strings in the same order: {messages}",
            },
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    parsed = __import__("json").loads(content)
    translated = parsed.get("translations")
    if not isinstance(translated, list):
        raise ValueError("Invalid translation response")
    return translated


if __name__ == "__main__":
    pass
