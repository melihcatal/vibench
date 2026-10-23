import os
from google.cloud import translate_v2 as translate


def translate_markup(
    html_content: str, target_language: str = "es", source_language: str = "en"
) -> str:
    """
    Translate HTML or markup content while preserving tags using Google Cloud Translation.

    Args:
        html_content: HTML or markup content to translate
        target_language: Target language code (default: "es" for Spanish)
        source_language: Source language code (default: "en" for English)

    Returns:
        Translated HTML/markup with tags preserved
    """
    client = translate.Client()

    result = client.translate(
        html_content,
        target_language=target_language,
        source_language=source_language,
        format_="html",
    )

    return result["translatedText"]
