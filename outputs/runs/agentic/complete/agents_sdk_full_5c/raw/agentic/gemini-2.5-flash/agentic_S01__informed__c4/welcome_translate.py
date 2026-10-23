import os
from google.cloud import translate_v2 as translate

def translate_welcome_message(text: str, target_language: str = "es"):
    """Translates text into the target language using Google Cloud Translation."""
    # Instantiates a client
    translate_client = translate.Client()

    # The Google Cloud project ID is usually inferred from the environment
    # (GOOGLE_APPLICATION_CREDENTIALS) or client configuration.

    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language
    }

