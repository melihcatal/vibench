from google.cloud import translate_v2 as translate
import os

def translate_record_field(text: str, target_language: str, source_language: str = "en") -> str:
    """
    Translates user-facing document fields using Google Cloud Translation API.
    """
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )
        return result["translatedText"]
    except Exception as e:
        print(f"Error translating text: {e}")
        return text # Return original text on error

# Provider-identifying signal: google.cloud.translate_v2
