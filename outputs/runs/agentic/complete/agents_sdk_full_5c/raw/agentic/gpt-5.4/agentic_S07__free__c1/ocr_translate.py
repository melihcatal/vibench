from __future__ import annotations

from document_client import coerce_text, get_text_translation_client
from document_models import TranslationResult


def translate_ocr_text(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    client = get_text_translation_client()
    response = client.translate(body=[{"text": coerce_text(text)}], to_language=[target_language], from_language=source_language)
    item = response[0] if response else {}
    translations = item.get("translations", []) if isinstance(item, dict) else item.translations
    detected = item.get("detectedLanguage", {}) if isinstance(item, dict) else getattr(item, "detected_language", None)
    translated_text = translations[0]["text"] if isinstance(translations[0], dict) else translations[0].text
    detected_language = detected.get("language") if isinstance(detected, dict) else getattr(detected, "language", source_language)
    return TranslationResult(
        provider="azure-ai-translator",
        translated_text=translated_text,
        source_language=detected_language,
        target_language=target_language,
        raw=item if isinstance(item, dict) else {"translations": [getattr(t, "text", "") for t in translations]},
    )
