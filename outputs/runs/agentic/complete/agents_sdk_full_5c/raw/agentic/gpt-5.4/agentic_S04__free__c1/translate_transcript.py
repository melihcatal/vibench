from __future__ import annotations

import os
from typing import Dict, Iterable, List, Optional

import requests

from speech_models import TranslationSegment

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_transcript(
    segments: Iterable[str],
    target_language: str,
    *,
    api_key: Optional[str] = None,
    source_language: Optional[str] = None,
) -> Dict[str, object]:
    auth_key = api_key or os.getenv("DEEPL_API_KEY")
    if not auth_key:
        raise ValueError("DEEPL_API_KEY is required")
    texts = [segment for segment in segments if segment]
    payload = {"text": texts, "target_lang": target_language}
    if source_language:
        payload["source_lang"] = source_language
    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    translated: List[TranslationSegment] = []
    for source_text, item in zip(texts, data.get("translations", [])):
        translated.append(
            TranslationSegment(
                source_text=source_text,
                translated_text=item.get("text", ""),
                target_language=target_language,
            )
        )
    return {
        "provider": "deepl",
        "target_language": target_language,
        "translations": [segment.__dict__ for segment in translated],
    }
