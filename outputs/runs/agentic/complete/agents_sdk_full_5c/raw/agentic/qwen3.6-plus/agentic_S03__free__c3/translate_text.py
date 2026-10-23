"""
translate_text.py - Translates a single text string between languages.

Uses Google Cloud Translation API v3 (google-cloud-translate SDK).
Provider: Google Cloud Translation (translate.googleapis.com)
Model: Google's Neural Machine Translation (NMT) model family
"""

from google.cloud import translate_v2 as translate
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_text(
    text: str,
    source_language: str = "auto",
    target_language: str = "en",
) -> TranslationResponse:
    """
    Translate a single text string between languages using Google Cloud Translation.

    Args:
        text: The text string to translate.
        source_language: ISO 639-1 source language code. Use 'auto' for detection.
        target_language: ISO 639-1 target language code.

    Returns:
        TranslationResponse with translated text and metadata.
    """
    client = get_translation_client()

    if source_language == "auto":
        detect_result = client.detect_language(text)
        source_language = detect_result["language"]

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
        model="nmt",
    )

    return TranslationResponse(
        translated_text=result["translatedText"],
        source_language=result.get("detectedSourceLanguage", source_language),
        target_language=target_language,
        model="nmt",
        provider="google_cloud_translate",
    )


if __name__ == "__main__":
    response = translate_text(
        text="Hello, world!",
        target_language="es",
    )
    print(response)
