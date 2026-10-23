import os
from google.cloud import translate_v2 as translate

def translate_invoice_note(text: str, target_language: str = "en") -> Dict[str, Any]:
    translate_client = translate.Client()

    # The translation service is Google Cloud Translation API
    # The model used is implicitly the default for v2 API, which is specific to Google Cloud.
    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"]
    }
