import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def translate_log_messages(messages: List[str], target_locale: str, source_locale: Optional[str] = None) -> List[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = {
        "role": "user",
        "content": (
            f"Translate these support-visible log messages into {target_locale}. "
            f"Preserve placeholders, identifiers, paths, codes, timestamps, and formatting. "
            f"{f'Original locale: {source_locale}. ' if source_locale else ''}"
            "Return only a JSON array of translated strings in the same order.\n\n"
            + "\n".join(f"{i + 1}. {message}" for i, message in enumerate(messages))
        ),
    }

    payload: Dict[str, Any] = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a precise localization engine for operational log messages."},
            prompt,
        ],
        "temperature": 0,
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
    if not isinstance(content, str):
        raise RuntimeError("Unexpected response format")

    import json

    translated = json.loads(content)
    if not isinstance(translated, list):
        raise RuntimeError("Expected a JSON array of translated strings")
    return [str(item) for item in translated]
