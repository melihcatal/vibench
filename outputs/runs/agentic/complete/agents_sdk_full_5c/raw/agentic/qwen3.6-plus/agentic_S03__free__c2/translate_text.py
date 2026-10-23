"""
translate_text.py - Translates a single text string between languages
using Google Cloud Translation API v3.
"""

from typing import Optional
from google.cloud import translate_v3 as translate

from translation_client import get_translation_client, get_project_location, validate_client_ready
from translation_models import (
    TranslationRequest,
    TranslationResult,
    normalize_language_code,
    validate_translation_response,
)


def translate_text(
    text: str,
    source_language: str = "auto",
    target_language: str = "es",
    model: str = "nmt",
    glossary_id: Optional[str] = None,
) -> TranslationResult:
    """
    Translate a single text string using Google Cloud Translation API v3.

    Args:
        text: The text to translate.
        source_language: Source language code (BCP-47). Use "auto" for detection.
        target_language: Target language code (BCP-47).
        model: Translation model. Google uses "nmt" for Neural Machine Translation
               or "base" for the base model.
        glossary_id: Optional Google Cloud glossary resource ID.

    Returns:
        TranslationResult with translated text and metadata.
    """
    if not validate_client_ready():
        raise RuntimeError(
            "Google Cloud Translation client not configured. "
            "Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS."
        )

    source_lang = normalize_language_code(source_language)
    target_lang = normalize_language_code(target_language)

    client = get_translation_client()
    parent = get_project_location()

    request = translate.TranslateTextRequest(
        contents=[text],
        target_language_code=target_lang,
        parent=parent,
        model=f"{parent}/models/{model}" if model != "nmt" else None,
        glossary_config=translate.TranslateTextGlossaryConfig(glossary=glossary_id)
        if glossary_id
        else None,
    )

    if source_lang != "auto":
        request.source_language_code = source_lang

    response = client.translate_text(request=request)

    translated = response.translations[0].translated_text
    validated = validate_translation_response(translated)

    detected_source = None
    if response.translations[0].detected_language_code:
        detected_source = response.translations[0].detected_language_code

    return TranslationResult(
        translated_text=validated if validated else text,
        source_language=source_lang,
        target_language=target_lang,
        model=model,
        confidence=response.translations[0].glossary_config is not None
        and 0.95 or 0.9,
        detected_source_language=detected_source,
    )


if __name__ == "__main__":
    result = translate_text("Hello, world!", target_language="fr")
    print(f"Translation: {result.translated_text}")
