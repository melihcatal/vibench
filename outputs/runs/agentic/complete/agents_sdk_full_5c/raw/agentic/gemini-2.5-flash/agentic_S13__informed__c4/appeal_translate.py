import os
from google.cloud import translate_v2 as translate

def translate_appeal_text(text: str, target_language: str = "en"):
    """
    Translate appeal text for review using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS not set. Translation might fail.")

    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"]
        }
    except Exception as e:
        print(f"Error translating appeal text with Google Cloud Translation: {e}")
        return None
