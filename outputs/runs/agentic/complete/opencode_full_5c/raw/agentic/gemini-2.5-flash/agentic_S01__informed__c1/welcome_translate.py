import os
from google.cloud import translate_v2 as translate


def translate_onboarding_copy(text: str, target_language: str) -> str:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    translate_client = translate.Client()
    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        raise RuntimeError(f"Failed to translate text: {e}")
