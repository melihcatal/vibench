from __future__ import annotations

import os

import httpx

from speech_models import TranscriptChunk


async def translate_live_caption(chunk: TranscriptChunk, target_language: str) -> dict:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_API_KEY is required for DeepL translation")
    async with httpx.AsyncClient(base_url="https://api.deepl.com") as client:
        response = await client.post(
            "/v2/translate",
            data={
                "text": chunk.text,
                "target_lang": target_language.upper(),
                "source_lang": (chunk.language_code or "EN").split("-")[0].upper(),
            },
            headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        )
        response.raise_for_status()
        payload = response.json()
    translations = payload.get("translations", [])
    translated_text = translations[0]["text"] if translations else ""
    return {
        "provider": "deepl",
        "target_language": target_language,
        "text": translated_text,
        "source_text": chunk.text,
    }
