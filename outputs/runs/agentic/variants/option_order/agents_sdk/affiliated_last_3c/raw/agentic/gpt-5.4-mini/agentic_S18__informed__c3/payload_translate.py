from __future__ import annotations

from deepl import Translator

from messaging_models import TranslationResult, ensure_text


TARGET_LANG = "DE"


def payload_translate(text: str, source_language: str = "EN", target_language: str = TARGET_LANG) -> TranslationResult:
    translator = Translator(auth_key=__import__("os").getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(ensure_text(text), source_lang=source_language, target_lang=target_language)
    return TranslationResult(
        source_text=ensure_text(text),
        translated_text=ensure_text(result.text),
        source_language=source_language,
        target_language=target_language,
        provider="deepl",
    )
