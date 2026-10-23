import os
from google.cloud import translate_v2 as translate
from storage_client import ManagedStorageClient


def translate_extracted_text(source_text: str, target_lang: str = "en") -> dict:
    """Translate extracted document text using Google Cloud Translation.

    Returns the translated text and detected source language.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        raise RuntimeError(
            "Google credentials not configured (missing GOOGLE_APPLICATION_CREDENTIALS)"
        )
    translator = translate.Client()
    try:
        result = translator.translate(source_text, target_language=target_lang)
        return {
            "translated_text": result["translatedText"],
            "source_language": result["detectedSourceLanguage"],
        }
    except Exception as e:
        raise RuntimeError(f"Translation failed: {e}")
