from google.cloud import translate_v2 as translate
import os


def translate_text(text, target_language="en", source_language=None):
    """
    Translate a single text string between languages using Google Cloud Translation.

    Args:
        text: The text to translate
        target_language: Target language code (default: 'en')
        source_language: Source language code (optional, auto-detected if None)

    Returns:
        Translated text string
    """
    client = translate.Client()

    if source_language:
        result = client.translate(
            text, target_language=target_language, source_language=source_language
        )
    else:
        result = client.translate(text, target_language=target_language)

    return result["translatedText"]
