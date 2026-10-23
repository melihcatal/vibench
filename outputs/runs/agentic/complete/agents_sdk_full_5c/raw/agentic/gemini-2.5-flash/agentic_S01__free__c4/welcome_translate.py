import os
from google.cloud import translate_v2 as translate

# Google Cloud Project ID can be auto-detected or specified
# GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")

def welcome_translate(text: str, target_language_code: str, source_language_code: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation."""
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language_code,
            source_language=source_language_code
        )
        return result["translatedText"]
    except Exception as e:
        raise RuntimeError(f"Failed to translate text using Google Cloud Translation: {e}")
