import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _build_prompt(query: str, target_language: str) -> str:
    return (
        f"Translate the following search query into {target_language}. "
        "Preserve named entities, product names, code, and search intent. "
        "Return only the translated query text.\n\n"
        f"Query: {query}"
    )


def translate_query(query: str, target_language: str = "English", api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a precise translation engine for search queries."},
            {"role": "user", "content": _build_prompt(query, target_language)},
        ],
        "temperature": 0,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
