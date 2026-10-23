import os
from typing import Dict, Any, List
from google.cloud import translate_v2 as translate

def translate_appeal_text(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    # Google Cloud credentials are typically handled by GOOGLE_APPLICATION_CREDENTIALS
    # or by running in a Google Cloud environment.
    # Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # the application is running in a GCP environment with appropriate permissions.

    client = translate.Client()

    text_to_translate = payload["text"]
    target_language = payload.get("target_language", "en")
    source_language = payload.get("source_language", None) # Auto-detect if None

    # The client.translate method returns a dictionary with the translated text and other metadata.
    translation_result = client.translate(
        text_to_translate,
        target_language=target_language,
        source_language=source_language
    )

    translated_text = translation_result["translatedText"]
    detected_source_language = translation_result.get("detectedSourceLanguage")

    return {
        "original_text": text_to_translate,
        "translated_text": translated_text,
        "target_language": target_language,
        "detected_source_language": detected_source_language
    }
