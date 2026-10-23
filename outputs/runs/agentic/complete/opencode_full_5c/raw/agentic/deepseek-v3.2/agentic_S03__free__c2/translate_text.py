import os
from translation_client import TranslationClient


def translate_text(text: str, source_lang: str = "en", target_lang: str = "es") -> str:
    """
    Translate a single text string between languages using Google Cloud Translation API.

    Args:
        text: The text to translate
        source_lang: Source language code (default: "en")
        target_lang: Target language code (default: "es")

    Returns:
        Translated text string
    """
    client = TranslationClient()

    # Use Google Cloud Translation API
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(
        text, source_language=source_lang, target_language=target_lang
    )

    return result["translatedText"]
