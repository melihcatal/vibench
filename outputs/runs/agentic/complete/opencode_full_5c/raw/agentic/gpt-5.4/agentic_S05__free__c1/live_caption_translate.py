from __future__ import annotations

import os
from typing import Iterable, List

import requests


def translate_live_captions(captions: Iterable[str], target_language: str) -> List[str]:
    api_key = os.environ["DEEPL_API_KEY"]
    url = "https://api-free.deepl.com/v2/translate"
    translated: List[str] = []
    for caption in captions:
        response = requests.post(
            url,
            headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
            data={"text": caption, "target_lang": target_language},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        translated.append(payload["translations"][0]["text"])
    return translated
