from __future__ import annotations

import os

import requests

from embeddings_client import DEFAULT_MULTILINGUAL_MODEL


DEEPL_TRANSLATE_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY_ENV = "DEEPL_API_KEY"


def translate_query(query: str, target_language: str = "EN") -> dict[str, str]:
    api_key = os.environ[DEEPL_API_KEY_ENV]
    response = requests.post(
        DEEPL_TRANSLATE_URL,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data={"text": query, "target_lang": target_language},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    translation = payload.get("translations", [{}])[0]
    return {
        "translated_text": translation.get("text", ""),
        "detected_source_language": translation.get("detected_source_language", ""),
        "embedding_model": DEFAULT_MULTILINGUAL_MODEL,
    }
