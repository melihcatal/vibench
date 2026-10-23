import os
from google.cloud import translate_v2 as translate
from speech_models import TranslationResult

def translate_caption(text: str, target_language: str = "fr") -> TranslationResult:
    """
    Translates a live caption text to another language using Google Cloud Translate.

    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return TranslationResult(
        original_text=text,
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"],
    )
