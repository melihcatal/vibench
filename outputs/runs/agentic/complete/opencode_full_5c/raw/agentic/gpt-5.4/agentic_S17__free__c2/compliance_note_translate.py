from __future__ import annotations

from security_client import post_google_translate
from security_models import TranslationResult


def compliance_note_translate(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    payload = {"q": text, "target": target_language, "format": "text"}
    if source_language:
        payload["source"] = source_language
    response = post_google_translate(payload)
    translation = response["data"]["translations"][0]
    return TranslationResult(
        provider="google-translate",
        source_language=source_language,
        target_language=target_language,
        translated_text=translation["translatedText"],
    )
