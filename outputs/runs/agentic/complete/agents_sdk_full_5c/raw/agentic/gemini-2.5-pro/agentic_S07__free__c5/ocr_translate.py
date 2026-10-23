# ocr_translate.py
import os
from google.cloud import translate_v2 as translate
from document_models import TranslationResponse

def translate_text(text: str, target_language: str = "en") -> TranslationResponse:
    """
    Translates text using the Google Cloud Translation API.
    
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_language_code=result["detectedSourceLanguage"],
    )
