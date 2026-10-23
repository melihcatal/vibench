"""
translate_markup.py - Translates HTML or markup while preserving tags.

Uses Google Cloud Translation API v2 (google-cloud-translate SDK).
Provider: Google Cloud Translation (translate.googleapis.com)
Model: Google's Neural Machine Translation (NMT) model family
"""

from google.cloud import translate_v2 as translate
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_markup(
    markup: str,
    source_language: str = "auto",
    target_language: str = "en",
) -> TranslationResponse:
    """
    Translate HTML or markup while preserving tags using Google Cloud Translation.

    The format_="html" parameter ensures HTML tags are preserved and not translated.

    Args:
        markup: The HTML or markup string to translate.
        source_language: ISO 639-1 source language code. Use 'auto' for detection.
        target_language: ISO 639-1 target language code.

    Returns:
        TranslationResponse with translated markup and metadata.
    """
    client = get_translation_client()

    if source_language == "auto":
        detect_result = client.detect_language(markup)
        source_language = detect_result["language"]

    result = client.translate(
        markup,
        target_language=target_language,
        source_language=source_language,
        format_="html",
        model="nmt",
    )

    return TranslationResponse(
        translated_text=result["translatedText"],
        source_language=result.get("detectedSourceLanguage", source_language),
        target_language=target_language,
        model="nmt",
        provider="google_cloud_translate",
        content_type="html",
    )


if __name__ == "__main__":
    html = "<p>Hello, <strong>world</strong>!</p>"
    response = translate_markup(html, target_language="de")
    print(response)
