import os

import deepl

from model_models import TranslationResult, normalize_text


def translate_result(
    text: str, target_language: str, source_language: str | None = None
) -> dict:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        normalize_text(text),
        target_lang=target_language,
        source_lang=source_language,
    )
    normalized = TranslationResult(
        provider="DeepL",
        translated_text=result.text,
        detected_source_language=getattr(
            result, "detected_source_lang", source_language
        ),
        target_language=target_language,
    )
    return {
        "provider": normalized.provider,
        "translated_text": normalized.translated_text,
        "detected_source_language": normalized.detected_source_language,
        "target_language": normalized.target_language,
    }
