"""Translate a single text string between languages using Google Cloud Translation API."""

import os
from google.cloud import translate_v2 as translate
from translation_client import load_translation_config, create_translation_client
from translation_models import TranslationRequest, TranslationResponse, normalize_language_code


def translate_text(source_text: str, source_lang: str, target_lang: str) -> TranslationResponse:
    """Translate a single text string using Google Cloud Translation.

    Args:
        source_text: The text to translate.
        source_lang: Source language code (e.g., 'en', 'fr', 'ja').
        target_lang: Target language code.

    Returns:
        TranslationResponse with translated text and metadata.
    """
    config = load_translation_config()
    client = create_translation_client(provider="google")

    normalized_source = normalize_language_code(source_lang)
    normalized_target = normalize_language_code(target_lang)

    request = TranslationRequest(
        text=source_text,
        source_lang=normalized_source,
        target_lang=normalized_target,
        model="nmt",
    )

    result = client.translate(
        request.text,
        target_language=request.target_lang,
        source_language=request.source_lang if request.source_lang != "auto" else None,
        format_="text",
        model=request.model,
    )

    detected_source = result.get("detectedSourceLanguage", request.source_lang)
    translated_text = result.get("translatedText", "")

    response = TranslationResponse(
        translated_text=translated_text,
        source_lang=detected_source,
        target_lang=request.target_lang,
        model_used="google-nmt",
        confidence=1.0,
        character_count=len(source_text),
    )

    return response


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 4:
        text = sys.argv[1]
        src = sys.argv[2]
        tgt = sys.argv[3]
        result = translate_text(text, src, tgt)
        print(result.translated_text)
    else:
        print("Usage: translate_text.py <text> <source_lang> <target_lang>")
