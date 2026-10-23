import os
from google.cloud import translate_v2 as translate

def translate_payload(text: str, target_language: str = "es") -> str:
    """
    Translates customer-facing text in a payload using Google Cloud Translate.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    try:
        translate_client = translate.Client()

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        result = translate_client.translate(text, target_language=target_language)
        
        translated_text = result["translatedText"]
        detected_language = result["detectedSourceLanguage"]
        
        print(f"Translated '{text}' from {detected_language} to {target_language}: '{translated_text}'")
        
        return translated_text

    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return f"Translation failed: {text}"
