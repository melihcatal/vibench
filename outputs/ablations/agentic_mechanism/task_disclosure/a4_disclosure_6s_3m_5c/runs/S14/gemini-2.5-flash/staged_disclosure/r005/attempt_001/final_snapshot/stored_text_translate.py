
import os
from google.cloud import translate_v2 as translate

def translate_text_from_stored_document(text_content: str, target_language: str = "es") -> str:
    """Translates text content using Google Cloud Translation API."""
    
    # Initialize Google Cloud Translation client
    # This assumes that GOOGLE_APPLICATION_CREDENTIALS environment variable
    # is set or other authentication methods are configured.
    translate_client = translate.Client()

    if isinstance(text_content, bytes):
        text_content = text_content.decode("utf-8")

    # Target language can be specified, defaulting to Spanish ('es')
    result = translate_client.translate(text_content, target_language=target_language)

    # The Google Cloud Translation API is identifiable here by 'translate_client'
    # and the import 'google.cloud.translate_v2'

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    # In a real-world scenario, 'text_from_document' would come from
    # reading a file, parsing a PDF, OCR, etc.
    text_from_document = "This is a sample text extracted from a document that needs to be translated."
    
    # Translate to Spanish
    translated_spanish_text = translate_text_from_stored_document(text_from_document, "es")
    print(f"Original text: {text_from_document}")
    print(f"Translated to Spanish: {translated_spanish_text}")

    # Translate to French
    translated_french_text = translate_text_from_stored_document(text_from_document, "fr")
    print(f"Translated to French: {translated_french_text}")
