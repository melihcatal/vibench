from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

import requests


DEEPL_API_BASE = "https://api.deepl.com/v2/translate"


def translate_transcript_segments(
    segments: Iterable[str], target_language: str, source_language: str | None = None
) -> Dict[str, Any]:
    text_segments = list(segments)
    response = requests.post(
        DEEPL_API_BASE,
        headers={
            "Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}",
        },
        data={
            "target_lang": target_language,
            **({"source_lang": source_language} if source_language else {}),
            **{f"text[{index}]": value for index, value in enumerate(text_segments)},
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    translations: List[str] = [item["text"] for item in payload.get("translations", [])]
    return {
        "provider": "DeepL",
        "endpoint": DEEPL_API_BASE,
        "translations": translations,
    }
