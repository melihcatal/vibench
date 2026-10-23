import boto3
import json
from typing import Dict, Any
from messaging_client import get_translate_client

def translate_message_payload_text(text_to_translate: str, source_language: str, target_language: str) -> Dict[str, Any]:
    """
    Translates customer-facing message payload text using AWS Translate.
    """
    translate_client = get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        translated_text = response.get('TranslatedText')
        
        print(f"Original ({source_language}): {text_to_translate}")
        print(f"Translated ({target_language}): {translated_text}")

        return {
            "original_text": text_to_translate,
            "translated_text": translated_text,
            "source_language": source_language,
            "target_language": target_language
        }

    except Exception as e:
        print(f"Error translating text with AWS Translate: {e}")
        raise

if __name__ == "__main__":
    english_text = "Hello, how are you today?"
    spanish_text = "Hola, ¿cómo estás hoy?"

    print("\nTranslating English to Spanish:")
    translate_message_payload_text(english_text, "en", "es")

    print("\nTranslating Spanish to English:")
    translate_message_payload_text(spanish_text, "es", "en")

    print("\nTranslating English to French:")
    translate_message_payload_text("Good morning!", "en", "fr")
