from google.cloud import translate_v2 as translate
import os

# Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
# Ensure this environment variable is set or configure ADC.

def translate_consent_copy(text: str, target_language: str, source_language: str = None) -> dict:
    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language, source_language=source_language)
        return {
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"],
            "target_language": target_language,
        }
    except Exception as e:
        return {"error": str(e)}
