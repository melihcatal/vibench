import os
from typing import Any, Dict, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


def _translate_with_openai(query: str, target_language: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    if not query.strip():
        raise ValueError("query must not be empty")

    language_prompt = (
        f"Translate the query into {target_language}."
        if target_language
        else "Translate the query into English."
    )
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_TRANSLATION_MODEL,
            "messages": [
                {"role": "system", "content": "You translate search queries faithfully and concisely."},
                {"role": "user", "content": f"{language_prompt} Preserve meaning. Return only the translated query.\n\nQuery: {query}"},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def multilingual_query_translate(query: str, target_language: Optional[str] = None) -> Dict[str, Any]:
    translated_query = _translate_with_openai(query, target_language=target_language)
    return {
        "provider": "openai",
        "model": OPENAI_TRANSLATION_MODEL,
        "original_query": query,
        "translated_query": translated_query,
        "target_language": target_language or "en",
    }
