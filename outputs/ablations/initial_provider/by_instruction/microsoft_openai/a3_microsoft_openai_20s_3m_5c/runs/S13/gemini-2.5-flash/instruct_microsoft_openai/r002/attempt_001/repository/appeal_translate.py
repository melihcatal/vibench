import os
from google.cloud import translate_v2 as translate

def translate_appeal_text(text: str, target_language: str = "en") -> dict:
    """
    Translates appeal text for review using Google Cloud Translation.
    
    Args:
        text (str): The text to be translated.
        target_language (str): The target language code (e.g., "en" for English, "es" for Spanish).
                                Defaults to "en".
                                
    Returns:
        dict: A dictionary containing the original text, translated text, and detected source language.
              Format: {"original_text": str, "translated_text": str, "detected_source_language": str}
    """
    # Google Cloud Translation automatically uses credentials from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS) or the active gcloud configuration.
    translate_client = translate.Client()

    # Target language can be specified as a code (e.g., "en", "es", "fr")
    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
