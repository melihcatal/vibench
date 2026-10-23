from google.cloud import translate_v2 as translate
import re


def translate_markup(html_content, target_language="en", source_language=None):
    """
    Translate HTML or markup content while preserving tags using Google Cloud Translation.

    Args:
        html_content: HTML/markup string to translate
        target_language: Target language code (default: 'en')
        source_language: Source language code (optional, auto-detected if None)

    Returns:
        Translated HTML/markup string with tags preserved
    """
    client = translate.Client()

    if source_language:
        result = client.translate(
            html_content,
            target_language=target_language,
            source_language=source_language,
            format_="html",
        )
    else:
        result = client.translate(
            html_content, target_language=target_language, format_="html"
        )

    return result["translatedText"]
