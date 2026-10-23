from typing import Dict
from safety_models import AppealTranslation
from google.cloud import translate_v2 as translate
import os


def translate_appeal(text: str, target_language: str = "en") -> AppealTranslation:
    """Translate appeal text for review using Google Cloud Translation."""
    client = translate.Client()

    result = client.translate(text, target_language=target_language)

    return AppealTranslation(
        original_text=text,
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"],
        target_language=target_language,
    )
