from __future__ import annotations

import os
from typing import Any, Dict

import httpx


DEEPL_API_URL = "https://api.deepl.com/v2/translate"


async def translate_live_caption(
    text: str, target_language: str, source_language: str | None = None
) -> Dict[str, Any]:
    payload = {"text": [text], "target_lang": target_language}
    if source_language:
        payload["source_lang"] = source_language
    headers = {"Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(DEEPL_API_URL, data=payload, headers=headers)
        response.raise_for_status()
        body = response.json()
    translation = body["translations"][0]
    return {
        "provider": "deepl",
        "translated_text": translation["text"],
        "detected_source_language": translation.get("detected_source_language"),
    }
