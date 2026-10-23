import os
from google.cloud import translate_v2 as translate

def translate_consent_copy(text: str, target_language: str = "en", source_language: str = "auto") -> dict:
    # Initialize Google Cloud Translation API client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set

    try:
        client = translate.Client()

        if source_language == "auto":
            result = client.translate(text, target_language=target_language)
        else:
            result = client.translate(text, target_language=target_language, source_language=source_language)

        return {
            "original_text": text,
            "translated_text": result['translatedText'],
            "source_language": result['detectedSourceLanguage'] if source_language == "auto" else source_language,
            "target_language": target_language
        }

    except Exception as e:
        return {"error": f"Google Cloud Translation API error: {e}"}
