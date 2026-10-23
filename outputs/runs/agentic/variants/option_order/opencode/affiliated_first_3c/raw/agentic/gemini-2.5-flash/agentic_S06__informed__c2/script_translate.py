import os
from google.cloud import translate_v2 as translate


def translate_script(text: str, target_language: str) -> str:
    """Translates narration scripts using Google Cloud Translation.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    client = translate.Client()

    # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected for authentication
    result = client.translate(text, target_language=target_language)

    return result["translatedText"]
