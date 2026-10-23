import os
import re
from translation_client import get_translation_client


def translate_markup(html_content, source_lang="en", target_lang="es"):
    """
    Translate HTML or markup content while preserving tags using Google Cloud Translation API.

    Args:
        html_content: HTML or markup string to translate
        source_lang: Source language code (default: "en")
        target_lang: Target language code (default: "es")

    Returns:
        Translated HTML/markup with tags preserved
    """
    client = get_translation_client()

    try:
        from google.cloud import translate_v2 as translate

        # Google Cloud Translation API automatically preserves HTML tags
        # when format='html' is specified
        result = client.translate(
            html_content,
            source_language=source_lang,
            target_language=target_lang,
            format_="html",
        )

        return result["translatedText"]

    except Exception as e:
        raise Exception(f"Markup translation failed: {str(e)}")
