from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

import requests


def record_translate(
    documents: Iterable[Dict[str, Any]], fields: List[str], target_language: str
) -> List[Dict[str, Any]]:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("Missing required environment variable: DEEPL_API_KEY")
    translated_documents: List[Dict[str, Any]] = []
    for document in documents:
        translated = dict(document)
        for field in fields:
            value = document.get(field)
            if not isinstance(value, str) or not value.strip():
                continue
            response = requests.post(
                "https://api.deepl.com/v2/translate",
                headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
                data={"text": value, "target_lang": target_language.upper()},
                timeout=30,
            )
            response.raise_for_status()
            translated[field] = response.json()["translations"][0]["text"]
        translated_documents.append(translated)
    return translated_documents
