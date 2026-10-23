import os
from typing import Optional
import deepl
from model_models import TranslationResult


def translate_result(
    text: str,
    target_language: str = "ES",
    source_language: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> TranslationResult:
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(key)

    translate_kwargs = {"target_lang": target_language}
    if source_language:
        translate_kwargs["source_lang"] = source_language

    result = translator.translate_text(text, **translate_kwargs)

    return TranslationResult(
        translated_text=result.text,
        source_language=result.detected_source_lang or source_language or "unknown",
        target_language=target_language,
    )
