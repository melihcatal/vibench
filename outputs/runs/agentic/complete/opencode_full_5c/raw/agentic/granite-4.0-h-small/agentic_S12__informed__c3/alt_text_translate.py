import os
from google.cloud import translate_v2 as translate
import json


def translate_alt_text(target_lang: str, alt_text: str) -> str:
    """Translate alt-text/description into another language using Google Cloud Translation.

    Args:
        target_lang: ISO language code (e.g., 'es', 'fr').
        alt_text: Original description string.

    Returns:
        Translated description string.
    """
    client = translate.Client()
    translation = client.translate(alt_text, target_language=target_lang)
    return translation["translatedText"]
