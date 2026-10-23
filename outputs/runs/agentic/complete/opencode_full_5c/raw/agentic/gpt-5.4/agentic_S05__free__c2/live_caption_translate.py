from __future__ import annotations

import os

import httpx


async def translate_live_caption(
    text: str, target_language: str, source_language: str = "en"
) -> dict[str, str]:
    endpoint = "https://api.deepl.com/v2/translate"
    api_key = os.environ["DEEPL_API_KEY"]
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            endpoint,
            data={
                "text": text,
                "source_lang": source_language.upper(),
                "target_lang": target_language.upper(),
            },
            headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        )
        response.raise_for_status()
    payload = response.json()
    translated = payload["translations"][0]["text"]
    return {
        "translated_text": translated,
        "provider": "api.deepl.com",
        "target_language": target_language,
    }
