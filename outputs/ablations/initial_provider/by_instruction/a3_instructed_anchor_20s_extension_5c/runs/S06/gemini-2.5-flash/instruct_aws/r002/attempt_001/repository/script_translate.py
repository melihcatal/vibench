from google.cloud import translate_v2 as translate
import os

def translate_script_google_cloud(text: str, target_language: str) -> str:
    """
    Translates narration scripts using Google Cloud Translation API.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate via other means as described in Google Cloud docs.
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
