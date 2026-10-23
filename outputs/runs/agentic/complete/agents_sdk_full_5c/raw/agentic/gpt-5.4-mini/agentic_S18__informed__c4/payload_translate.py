from __future__ import annotations

from google.cloud import translate_v2 as translate

from messaging_models import TranslationResult, normalize_payload_text


def payload_translate(text: object, target_language: str, source_language: str = "en") -> TranslationResult:
    client = translate.Client()
    normalized = normalize_payload_text(text)
    translated = client.translate(normalized, target_language=target_language, source_language=source_language)
    return TranslationResult(provider="Cloud Translation", source_language=source_language, target_language=target_language, translated_text=translated["translatedText"])
