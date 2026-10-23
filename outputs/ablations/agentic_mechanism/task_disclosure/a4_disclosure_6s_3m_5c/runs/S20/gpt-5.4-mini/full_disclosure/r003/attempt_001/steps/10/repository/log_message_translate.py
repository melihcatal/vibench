import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-5.4-mini"


def translate_log_messages(messages: List[str], target_locale: str, source_locale: Optional[str] = None, model: str = DEFAULT_MODEL, api_key: Optional[str] = None, timeout: int = 30) -> List[str]:
    if not messages:
        return []
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    system_prompt = "Translate support-visible log messages accurately, preserving placeholders, identifiers, timestamps, severity labels, and code-like tokens. Return only a JSON array of translated strings in the same order."
    user_payload: Dict[str, Any] = {
        "target_locale": target_locale,
        "messages": messages,
    }
    if source_locale:
        user_payload["source_locale"] = source_locale
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(user_payload)},
            ],
            "temperature": 0,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    if isinstance(content, list):
        content = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    import json

    translated = json.loads(content)
    if not isinstance(translated, list):
        raise ValueError("Expected a JSON array of translated strings")
    return [str(item) for item in translated]
