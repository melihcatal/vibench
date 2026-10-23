import json
import os
from typing import Dict, Any
from messaging_client import get_translate_client
from messaging_models import TranslationRequest

def translate_payload_text(translation_request: TranslationRequest) -> Dict[str, Any]:
    """Translates customer-facing message payload text using AWS Translate.

    Args:
        translation_request: An instance of TranslationRequest containing the text,
                                 source language code, and target language code.

    Returns:
        A dictionary containing the translated text and metadata.
    """
    translate_client = get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=translation_request.text,
            SourceLanguageCode=translation_request.source_language_code,
            TargetLanguageCode=translation_request.target_language_code
        )
        return response
    except Exception as e:
        print(f"Error translating text with AWS Translate: {e}")
        raise

if __name__ == '__main__':
    # Example Usage (requires AWS credentials and AWS_REGION environment variable)
    # export AWS_REGION="us-east-1"

    sample_text_en = "Hello, how are you? Welcome to our service."
    sample_text_es = "Hola, ¿cómo estás? Bienvenido a nuestro servicio."

    # Translate English to Spanish
    translate_req_en_es = TranslationRequest(text=sample_text_en, source_language_code="en", target_language_code="es")
    print(f"Translating from {translate_req_en_es.source_language_code} to {translate_req_en_es.target_language_code}:\n\"{translate_req_en_es.text}\"")
    try:
        translation_result_en_es = translate_payload_text(translate_req_en_es)
        print(f"Translated Text: \"{translation_result_en_es.get('TranslatedText')}\"")
    except Exception as e:
        print(f"Failed to translate English to Spanish: {e}")

    print("\n" + "="*50 + "\n")

    # Translate Spanish to English
    translate_req_es_en = TranslationRequest(text=sample_text_es, source_language_code="es", target_language_code="en")
    print(f"Translating from {translate_req_es_en.source_language_code} to {translate_req_es_en.target_language_code}:\n\"{translate_req_es_en.text}\"")
    try:
        translation_result_es_en = translate_payload_text(translate_req_es_en)
        print(f"Translated Text: \"{translation_result_es_en.get('TranslatedText')}\"")
    except Exception as e:
        print(f"Failed to translate Spanish to English: {e}")
