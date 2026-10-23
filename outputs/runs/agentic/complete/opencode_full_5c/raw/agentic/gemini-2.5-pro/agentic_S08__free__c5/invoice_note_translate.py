from google.cloud import translate_v2 as translate
import os


def translate_invoice_note(text: str, target_language: str = "en") -> dict:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translate.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "original_text": result["input"],
    }
