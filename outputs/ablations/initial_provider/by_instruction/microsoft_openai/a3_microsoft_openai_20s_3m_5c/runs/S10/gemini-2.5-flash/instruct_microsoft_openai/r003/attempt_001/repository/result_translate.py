import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates generated model output using Google Cloud Translation.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    translate_client = translate.Client()

    response = translate_client.translate(
        text,
        target_language=target_language
    )

    return response["translatedText"]
