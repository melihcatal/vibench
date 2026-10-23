import os
from google.cloud import translate_v2 as translate


def translate_consent_copy(text: str, target_language: str = 'en') -> str:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_TRANSLATE_CREDENTIALS_PATH")
    if not os.environ.get("GOOGLE_TRANSLATE_CREDENTIALS_PATH"):
        raise ValueError("Google Cloud Translation API credentials path must be set as an environment variable (GOOGLE_TRANSLATE_CREDENTIALS_PATH).")

    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']
