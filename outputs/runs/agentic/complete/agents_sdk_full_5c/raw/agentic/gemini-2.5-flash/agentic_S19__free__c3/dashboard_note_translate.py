from google.cloud import translate_v2 as translate
import os

def translate_dashboard_note(text: str, target_language: str):
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    translate_client = translate.Client()

    # The Google Cloud Translation API identifies itself through the client library
    # and the specific translate_v2 client.

    result = translate_client.translate(
        text,
        target_language=target_language
    )

    return result['translatedText']
