# [SAME-SCENARIO] translate_markup.py

import os
from google.cloud import translate_v2 as translate


def translate_markup(source_markup, target_language="es"):
    """Translate HTML/markup while preserving tags using Google Cloud Translation.

    This function sends the markup as-is; the translation service preserves tags.

    Args:
        source_markup (str): HTML or XML string to translate.
        target_language (str): Target language code (default: 'es').

    Returns:
        dict: Contains translated markup and provider identifier.
    """
    client = translate.Client()
    resp = client.translate(source_markup, target_language=target_language)
    return {
        "translated_markup": resp["translatedText"],
        "provider": "Google Cloud Translation",
        "model_id": "markup_translation",
    }
