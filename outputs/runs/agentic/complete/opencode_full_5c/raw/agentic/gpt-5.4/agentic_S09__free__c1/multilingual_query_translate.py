from __future__ import annotations

import os

import requests


DEEPL_API_BASE = "https://api-free.deepl.com/v2"


def multilingual_query_translate(
    query: str, target_language: str = "EN"
) -> dict[str, object]:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY is required")
    response = requests.post(
        f"{DEEPL_API_BASE}/translate",
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data={"text": query, "target_lang": target_language},
        timeout=30.0,
    )
    response.raise_for_status()
    body = response.json()
    translations = body.get("translations", [])
    translated_text = translations[0]["text"] if translations else ""
    detected_language = (
        translations[0].get("detected_source_language") if translations else None
    )
    return {
        "provider": "deepl",
        "target_language": target_language,
        "source_language": detected_language,
        "original_query": query,
        "translated_query": translated_text,
    }
