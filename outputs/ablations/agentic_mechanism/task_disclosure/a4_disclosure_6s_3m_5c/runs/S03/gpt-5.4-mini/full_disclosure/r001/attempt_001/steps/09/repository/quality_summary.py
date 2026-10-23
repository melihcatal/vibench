import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"


def _require_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key


def summarize_quality_issues(issues: List[Dict[str, Any]], locale: Optional[str] = None) -> str:
    api_key = _require_api_key()
    system_message = "You summarize translation quality issues concisely and clearly."
    user_message = {
        "locale": locale,
        "issues": issues,
    }
    payload = {
        "model": "gpt-5.4-mini",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": str(user_message)},
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def summarize_quality_issues_from_text(raw_issues: str, locale: Optional[str] = None) -> str:
    return summarize_quality_issues([{"raw": raw_issues}], locale=locale)
