from google.cloud import translate_v2 as translate
import os


def translate_consent_text(text: str, target_language: str) -> str:
    """
    Translates consent text using Google Cloud Translation.
    """
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
