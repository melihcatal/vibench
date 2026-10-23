import os
from google.cloud import translate_v2 as translate


def translate_onboarding_copy(text: str, target_locale: str) -> str:
    """Translate onboarding copy for the user's locale using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(text, target_language=target_locale)
    return result["translatedText"]
