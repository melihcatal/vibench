from typing import Dict


def translate_appeal_text(text: str, target_language: str = "en") -> Dict:
    """
    Translates appeal text for review using Google Cloud Translation API.
    Provider: Google Cloud Translation
    Model: google-translate-api
    """
    from google.cloud import translate_v2 as translate
    from google.oauth2 import service_account
    import os

    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    client = translate.Client(credentials=credentials)

    result = client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }
