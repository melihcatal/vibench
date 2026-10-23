import os
from translation_client import get_translation_client


def translate_text(text, source_lang="en", target_lang="es"):
    """
    Translate a single text string between languages using Google Cloud Translation API.

    Args:
        text: The text to translate
        source_lang: Source language code (default: "en")
        target_lang: Target language code (default: "es")

    Returns:
        Translated text string
    """
    client = get_translation_client()

    try:
        from google.cloud import translate_v2 as translate

        result = client.translate(
            text, source_language=source_lang, target_language=target_lang
        )

        return result["translatedText"]

    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")
