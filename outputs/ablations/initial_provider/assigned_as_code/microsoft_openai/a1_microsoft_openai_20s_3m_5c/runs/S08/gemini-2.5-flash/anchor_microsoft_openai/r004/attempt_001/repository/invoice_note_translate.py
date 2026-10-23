from google.cloud import translate_v2 as translate
from document_client import get_google_cloud_translate_config # For consistency

def translate_invoice_notes(text_content: str, target_language: str = 'en') -> dict:
    # Google Cloud client libraries typically handle authentication automatically
    client = translate.translate_client()

    result = client.translate(text_content, target_language=target_language)

    return {
        "original_text": text_content,
        "translated_text": result['translatedText'],
        "detected_source_language": result['detectedSourceLanguage'],
        "target_language": target_language
    }
