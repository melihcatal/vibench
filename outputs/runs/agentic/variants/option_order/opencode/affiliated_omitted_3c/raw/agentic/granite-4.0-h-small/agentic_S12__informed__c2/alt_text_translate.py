import os
from google.cloud import translate_v2 as translate


def translate_alt_text(description: str, target_lang: str = "es") -> str:
    """Translate a short image description into another language using Google Cloud Translation.
    Returns the translated text.
    """
    client = translate.Client()  # reads GOOGLE_APPLICATION_CREDENTIALS env var
    result = client.translate(description, target_language=target_lang)
    return result["translatedText"]
