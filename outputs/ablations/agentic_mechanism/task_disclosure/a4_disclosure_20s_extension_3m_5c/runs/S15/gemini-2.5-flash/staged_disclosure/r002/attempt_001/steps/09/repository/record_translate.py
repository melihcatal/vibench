import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation."""

    # Google Cloud Translation API client initialization
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage (replace with your actual document fields)
    document_field = "Hello, this is a document field to be translated."
    target_lang = "es"  # Spanish

    translated_field = translate_text(document_field, target_lang)

    print(f"Original: {document_field}")
    print(f"Translated ({target_lang}): {translated_field}")
