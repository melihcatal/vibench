import os
from google.cloud import translate_v2 as translate

def translate_welcome_message(text: str, target_language: str) -> str:
    # Google Cloud Translation API requires GOOGLE_APPLICATION_CREDENTIALS to be set
    # or run in a GCP environment with appropriate permissions.
    # The client will automatically pick up credentials from the environment.
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    # The 'translatedText' field contains the translated text
    # The 'detectedSourceLanguage' field contains the detected language of the original text
    return result['translatedText']
