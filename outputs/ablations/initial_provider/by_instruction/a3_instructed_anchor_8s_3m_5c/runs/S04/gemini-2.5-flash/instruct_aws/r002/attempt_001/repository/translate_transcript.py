from google.cloud import translate_v2 as translate
import os

def translate_text_with_google_cloud(text: str, target_language: str, source_language: str = "en") -> str:
    """
    Translates text using Google Cloud Translation API.
    """
    translate_client = translate.Client()

    result = translate_client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )

    return result['translatedText']
