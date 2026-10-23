import os
from google.cloud import translate_v2 as translate


def welcome_translate(text: str, locale: str = "en") -> str:
    """
    Translate onboarding copy into the user's locale using Google Cloud Translation.
    """
    client = translate.Client()
    result = client.translate(text, target_language=locale)
    return result["translatedText"]
