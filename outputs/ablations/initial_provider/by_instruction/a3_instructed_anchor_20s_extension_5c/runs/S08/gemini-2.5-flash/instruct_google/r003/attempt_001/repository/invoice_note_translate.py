import os
from google.cloud import translate_v2 as translate

def translate_invoice_notes(text_content: str, target_language: str = "en") -> Dict[str, Any]:
    client = translate.Client()

    # Google Cloud Translation API is provider-specific
    # The client automatically uses GOOGLE_APPLICATION_CREDENTIALS or other default credentials.

    result = client.translate(
        text_content, 
        target_language=target_language
    )

    translated_text = result['translatedText']
    detected_source_language = result['detectedSourceLanguage']

    return {
        "translated_text": translated_text,
        "detected_source_language": detected_source_language,
        "target_language": target_language,
        "raw_response": result
    }
