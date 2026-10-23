from google.cloud import translate_v2 as translate
import os
from typing import Optional


def translate_ocr_text(text: str, target_language: str = "en") -> Dict[str, str]:
    """Translates extracted OCR text using Google Cloud Translation API."""
    client = translate.Client()

    # Target language can be a language code, e.g. "en", "es", "fr", etc.
    result = client.translate(text, target_language=target_language)

    translated_text = result["translatedText"]
    original_language = result["detectedSourceLanguage"]
    
    return {"translated_text": translated_text, "original_language": original_language}

if __name__ == '__main__':
    # Placeholder for actual usage. Ensure GOOGLE_APPLICATION_CREDENTIALS is set.
    sample_text = "Hola mundo, esto es una prueba de traducción."
    target_lang = "en"

    try:
        # translated_output = translate_ocr_text(sample_text, target_lang)
        # print(f"Original Text: {sample_text}")
        # print(f"Detected Language: {translated_output["original_language"]}")
        # print(f"Translated Text ({target_lang}): {translated_output["translated_text"]}")
        print("Run with actual Google Cloud Translation credentials.")
    except Exception as e:
        print(f"Error translating text: {e}")
