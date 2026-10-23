"""Translate a list of strings while preserving order using DeepL API."""

import os
from deepl import Translator

from translation_models import TranslationRequest, TranslationResponse


def batch_translate(texts: list[str], target_lang: str, source_lang: str | None = None) -> list[TranslationResponse]:
    """Translate a list of strings preserving order using DeepL.

    Args:
        texts: List of text strings to translate.
        target_lang: Target language code (e.g., 'ES', 'FR', 'JA').
        source_lang: Source language code. If None, DeepL auto-detects.

    Returns:
        List of TranslationResponse objects in the same order as the input texts.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required for DeepL API access")

    translator = Translator(auth_key)

    kwargs: dict[str, str | None] = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    results = translator.translate_text(texts, **kwargs)

    responses: list[TranslationResponse] = []
    for result in results:
        responses.append(TranslationResponse(
            translated_text=result.text,
            source_lang=result.detected_source_lang if hasattr(result, "detected_source_lang") else source_lang or "auto",
            target_lang=target_lang,
            provider="deepl",
            model_id="deepl-free" if "api-free.deepl.com" in str(getattr(translator, "server_url", "")) else "deepl-pro",
        ))

    return responses
