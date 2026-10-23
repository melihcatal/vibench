import os
import requests

# Google Cloud Translation API credentials
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

from google.cloud import translate_v2 as translate

client = translate.Client()


def translate_text(source_text: str, target_lang: str = "en") -> str:
    """Translates generated model output to a target language.

    Args:
        source_text: The text produced by the LLM.
        target_lang: ISO-639-1 language code to translate to (default 'en').

    Returns:
        The translated string.
    """
    result = client.translate(source_text, target_language=target_lang)
    return result["translatedText"]
