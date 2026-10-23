from __future__ import annotations

from vision_client import get_deepl_translator
from vision_models import TranslationResult


PROVIDER = "deepl"


def alt_text_translate(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    translator = get_deepl_translator()
    result = translator.translate_text(text, target_lang=target_language, source_lang=source_language)
    detected_source = source_language or getattr(result, "detected_source_lang", None)
    return TranslationResult(
        provider=PROVIDER,
        translated_text=result.text,
        source_language=detected_source,
        target_language=target_language,
    )
