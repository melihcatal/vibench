from google.cloud import translate_v2 as translate
import os

def translate_compliance_note(text: str, target_language: str = 'es') -> str:
    """
    Translates encryption or compliance notes for reviewers using Google Cloud Translation.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set.
    translate_client = translate.Client()

    response = translate_client.translate(
        text,
        target_language=target_language
    )

    return response['translatedText']

