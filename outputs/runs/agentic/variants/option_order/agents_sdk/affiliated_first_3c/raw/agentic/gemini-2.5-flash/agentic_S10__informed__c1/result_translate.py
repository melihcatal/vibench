import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation: service=Cloud Translation; sdk=google-cloud-translate; interface=sdk; auth=GOOGLE_APPLICATION_CREDENTIALS

def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates generated model output using Google Cloud Translation.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # or application default credentials will be used.
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']
