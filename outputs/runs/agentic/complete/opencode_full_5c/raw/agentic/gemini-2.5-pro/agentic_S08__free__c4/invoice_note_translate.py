import os
from google.cloud import translate_v2 as translate
from document_models import TranslationResult


def invoice_note_translate(text: str, target_language: str = "en") -> TranslationResult:
    """
    Translates extracted invoice notes or descriptions using Google Cloud Translation.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return TranslationResult(
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"],
    )
