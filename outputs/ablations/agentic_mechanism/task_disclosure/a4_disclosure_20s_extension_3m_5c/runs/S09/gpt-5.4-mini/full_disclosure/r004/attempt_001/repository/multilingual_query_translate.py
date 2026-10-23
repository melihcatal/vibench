import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _build_messages(query: str, target_language: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You translate search queries for multilingual embedding retrieval. Return only the translated query.",
        },
        {
            "role": "user",
            "content": f"Translate this query into {target_language}: {query}",
        },
    ]


def translate_query(query: str, target_language: str = "English", api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": _build_messages(query, target_language),
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
