from __future__ import annotations

import os
from typing import Dict, Iterable, List, Optional

import requests

DEEPL_API_URL = "https://api.deepl.com/v2/translate"
DEEPL_API_KEY_ENV = "DEEPL_API_KEY"



def translate_transcript(segments: Iterable[str], target_lang: str, source_lang: Optional[str] = None) -> Dict[str, List[str]]:
    api_key = os.getenv(DEEPL_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"Missing API key in {DEEPL_API_KEY_ENV}")
    text_segments = list(segments)
    payload = {"text": text_segments, "target_lang": target_lang}
    if source_lang:
        payload["source_lang"] = source_lang
    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "provider": "DeepL",
        "translations": [item["text"] for item in data.get("translations", [])],
    }
