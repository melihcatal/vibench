import os
from typing import List

import requests


def batch_translate(strings: List[str], target_language: str) -> List[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    if not strings:
        return []

    prompt = (
        f"Translate the following list of strings into {target_language}. "
        "Preserve order and return only a JSON array of translated strings.\n"
        f"{strings}"
    )

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-5.4-mini",
            "messages": [
                {"role": "system", "content": "You translate text and return valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]

    import json

    translated = json.loads(content)
    if not isinstance(translated, list) or len(translated) != len(strings):
        raise ValueError("Invalid translation response")
    return translated
