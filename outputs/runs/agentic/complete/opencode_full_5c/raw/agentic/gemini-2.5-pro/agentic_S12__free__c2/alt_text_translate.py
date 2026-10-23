from google.cloud import translate_v2 as translate
from vision_models import Translation
import os


def translate_text(text: str, target_language: str) -> Translation:
    """Translates text to a target language using Google Cloud Translate API."""
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return Translation(
        translated_text=result["translatedText"],
        detected_language_code=result["detectedSourceLanguage"],
    )
