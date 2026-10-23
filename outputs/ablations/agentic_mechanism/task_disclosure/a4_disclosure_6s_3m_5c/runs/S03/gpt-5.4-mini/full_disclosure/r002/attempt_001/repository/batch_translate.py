import os
from typing import List, Optional

import requests


def batch_translate(strings: List[str], source_language: str, target_language: str, api_key: Optional[str] = None, model: str = "gpt-4o-mini") -> List[str]:
    if not strings:
        return []
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    f"Translate each item from {source_language} to {target_language}. "
                    "Return a JSON array of translated strings in the same order, with no extra text."
                ),
            },
            {"role": "user", "content": str(strings)},
        ],
        "temperature": 0,
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"].strip()
    if content.startswith("[") and content.endswith("]"):
        import json

        translated = json.loads(content)
        if isinstance(translated, list):
            return [str(item) for item in translated]
    raise ValueError("Unexpected translation response format")
