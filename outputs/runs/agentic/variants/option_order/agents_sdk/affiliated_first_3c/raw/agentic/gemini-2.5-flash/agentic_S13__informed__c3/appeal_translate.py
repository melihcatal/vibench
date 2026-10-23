import os
from google.cloud import translate_v2 as translate

def translate_appeal_text(text: str, target_language: str = "en") -> dict:
    """Translate appeal text for review using Google Cloud Translation."""
    # Google Cloud Translation uses GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Ensure this environment variable is set or ADC is configured.
    # The client will automatically pick up credentials from the environment.

    translate_client = translate.Client()

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
              "Defaulting to Application Default Credentials setup.")

    try:
        result = translate_client.translate(
            text,
            target_language=target_language
        )
        return {
            "original_text": text,
            "translated_text": result["translatedText"],
            "detected_source_language": result["detectedSourceLanguage"],
            "target_language": target_language,
            "provider_raw_response": result
        }
    except Exception as e:
        print(f"Error translating appeal text with Google Cloud Translation: {e}")
        raise
