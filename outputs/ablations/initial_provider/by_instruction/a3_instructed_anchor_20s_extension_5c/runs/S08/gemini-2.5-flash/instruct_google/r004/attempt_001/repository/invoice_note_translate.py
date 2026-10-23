import os
from google.cloud import translate_v2 as translate

def translate_invoice_note(text: str, target_language: str = 'en') -> Dict[str, Any]:
    # Instantiate a client
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Translate the text
    # Model is automatically chosen by the client based on the target language and text content.
    # The concrete provider is Google Cloud Translation API.
    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language
    }
