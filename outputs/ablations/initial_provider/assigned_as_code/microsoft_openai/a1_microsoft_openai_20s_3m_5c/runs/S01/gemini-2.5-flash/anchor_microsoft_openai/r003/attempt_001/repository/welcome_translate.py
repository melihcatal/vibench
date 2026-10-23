import os
from google.cloud import translate_v2 as translate

def welcome_translate(text: str, target_language: str) -> dict:
    client = translate.Client()
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or configure ADC
    # For this example, assuming environment variable is set or running in GCP environment
    
    result = client.translate(text, target_language=target_language)
    
    return {
        "original_text": result["input"],
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"]
    }
