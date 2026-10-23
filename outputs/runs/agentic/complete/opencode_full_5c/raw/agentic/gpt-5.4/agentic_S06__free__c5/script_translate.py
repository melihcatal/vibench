from __future__ import annotations

from speech_client import GOOGLE_TRANSLATE_URL, build_google_params, request_json
from speech_models import TranslationResult


def translate_script(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    payload = {
        "q": text,
        "target": target_language,
        "format": "text",
        "model": "nmt",
    }
    if source_language:
        payload["source"] = source_language
    response = request_json(
        "POST",
        GOOGLE_TRANSLATE_URL,
        params=build_google_params(),
        json=payload,
    )
    translation = response["data"]["translations"][0]
    return TranslationResult(
        translated_text=translation["translatedText"],
        source_language=translation.get("detectedSourceLanguage", source_language),
        target_language=target_language,
        provider="google-translate",
    )
