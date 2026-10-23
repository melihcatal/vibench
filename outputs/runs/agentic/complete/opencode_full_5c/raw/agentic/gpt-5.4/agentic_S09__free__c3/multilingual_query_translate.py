from __future__ import annotations

import os

import requests


def multilingual_query_translate(query: str, target_language: str = "English") -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "Translate search queries accurately while preserving retrieval intent.",
                },
                {
                    "role": "user",
                    "content": f"Translate this query to {target_language}: {query}",
                },
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translated = data["choices"][0]["message"]["content"].strip()
    return {
        "provider": "OpenAI",
        "model": "gpt-4o-mini",
        "source_query": query,
        "target_language": target_language,
        "translated_query": translated,
    }
