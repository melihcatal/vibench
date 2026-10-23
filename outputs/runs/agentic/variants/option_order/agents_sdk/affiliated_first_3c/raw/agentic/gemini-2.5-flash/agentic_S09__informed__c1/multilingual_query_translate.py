from google.cloud import translate_v2 as translate
import os
from typing import List, Dict, Any

def translate_query(text: str, target_language: str, source_language: str = None) -> Dict[str, Any]:
    """Translates a query text to a target language using Google Cloud Translation.

    Args:
        text: The query text to translate.
        target_language: The BCP-47 language code to translate to (e.g., 'es', 'fr').
        source_language: Optional. The BCP-47 language code of the input text.
                         If not provided, the service will attempt to detect it.

    Returns:
        A dictionary containing the translated text and detected source language.
        Example: {"translated_text": "Hola Mundo", "detected_source_language": "en"}
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or authenticated via gcloud
    # The client automatically picks up credentials from the environment.
    translate_client = translate.Client()

    try:
        # API hostname is implicitly googleapis.com/translate
        result = translate_client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )

        return {
            "translated_text": result['translatedText'],
            "detected_source_language": result['detectedSourceLanguage']
        }
    except Exception as e:
        print(f"Error translating query with Google Cloud Translation: {e}")
        return {"translated_text": text, "detected_source_language": source_language or "unknown", "error": str(e)}

