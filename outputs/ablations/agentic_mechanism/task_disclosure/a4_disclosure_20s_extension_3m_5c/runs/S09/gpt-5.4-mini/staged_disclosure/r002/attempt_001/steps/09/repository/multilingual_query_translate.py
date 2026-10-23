import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def _chat_completions(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def translate_query(query: str, target_language: str = "English") -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You translate search queries for multilingual embedding retrieval. "
                "Return only the translation, preserving named entities and query intent."
            ),
        },
        {
            "role": "user",
            "content": f"Translate the following query into {target_language}: {query}",
        },
    ]
    result = _chat_completions(
        {
            "model": OPENAI_TRANSLATION_MODEL,
            "messages": messages,
            "temperature": 0,
        }
    )
    return result["choices"][0]["message"]["content"].strip()


def translate_queries(queries: List[str], target_language: str = "English") -> List[str]:
    return [translate_query(query, target_language=target_language) for query in queries]


def translate_query_for_search(query: str, target_language: str = "English") -> Dict[str, str]:
    translated = translate_query(query, target_language=target_language)
    return {"original_query": query, "translated_query": translated, "target_language": target_language}
