from __future__ import annotations

import requests

from document_client import get_azure_translator_config
from document_models import TranslationResult


def translate_ocr_text(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    config = get_azure_translator_config()
    params = {"api-version": "3.0", "to": target_language}
    if source_language:
        params["from"] = source_language
    response = requests.post(
        f"{config['endpoint']}/translate",
        params=params,
        headers={
            "Ocp-Apim-Subscription-Key": config["key"],
            "Ocp-Apim-Subscription-Region": config["region"],
            "Content-Type": "application/json",
        },
        json=[{"text": text}],
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()[0]
    detected = payload.get("detectedLanguage", {}).get("language")
    translated = payload["translations"][0]["text"]
    return TranslationResult(
        provider="azure-ai-translator",
        translated_text=translated,
        detected_source_language=detected or source_language,
        target_language=target_language,
        raw=payload,
    )
