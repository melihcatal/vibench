# [HELPER] translation_client.py

import os
from google.cloud import translate_v2 as translate


def get_translation_client():
    """Return a configured Google Cloud Translation client.

    Credentials are read from the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    return translate.Client()


def translate_via_client(client, text, target_language="es"):
    """Translate using the provided client instance.

    Args:
        client: Pre‑configured translate.Client().
        text (str): Source text.
        target_language (str): Target language code.

    Returns:
        dict: Translation result with provider metadata.
    """
    result = client.translate(text, target_language=target_language)
    return {
        "translated_text": result["translatedText"],
        "provider": "Google Cloud Translation",
        "model_id": "general_text_translation",
    }
