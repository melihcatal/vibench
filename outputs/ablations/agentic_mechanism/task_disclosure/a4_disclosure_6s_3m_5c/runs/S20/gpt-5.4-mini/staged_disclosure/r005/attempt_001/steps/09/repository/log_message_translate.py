import os
from typing import List, Dict, Any

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_log_messages(messages: List[str], target_locale: str) -> List[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = (
        f"Translate these support-visible log messages into {target_locale}. "
        "Preserve technical identifiers, placeholders, and formatting. "
        "Return a JSON array of translated strings in the same order.\n\n"
        + "\n".join(f"- {message}" for message in messages)
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
                {"role": "system", "content": "You translate log messages accurately and concisely."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    content = data["choices"][0]["message"]["content"]
    return _parse_json_array(content)


def _parse_json_array(content: str) -> List[str]:
    import json

    parsed = json.loads(content)
    if not isinstance(parsed, list) or not all(isinstance(item, str) for item in parsed):
        raise ValueError("Translation response must be a JSON array of strings")
    return parsed
