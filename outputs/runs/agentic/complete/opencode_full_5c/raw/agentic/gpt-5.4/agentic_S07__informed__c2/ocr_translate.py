from __future__ import annotations

import requests

from document_client import get_translator_endpoint, get_translator_headers


def translate_ocr_text(
    text: str, target_language: str, source_language: str | None = None
) -> dict:
    params = {"api-version": "3.0", "to": target_language}
    if source_language:
        params["from"] = source_language
    response = requests.post(
        f"{get_translator_endpoint()}/translate",
        params=params,
        headers=get_translator_headers(),
        json=[{"text": text}],
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()[0]
    translation = (payload.get("translations") or [{}])[0]
    detected = payload.get("detectedLanguage") or {}
    return {
        "provider": "api.cognitive.microsofttranslator.com",
        "translated_text": translation.get("text", ""),
        "target_language": translation.get("to", target_language),
        "detected_language": detected.get("language", source_language),
        "raw": payload,
    }
