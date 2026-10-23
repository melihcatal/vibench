import os
from google.cloud import translate_v2 as translate
from typing import Dict
from .vision_models import AltTextTranslationRequest


def translate_alt_text(request: AltTextTranslationRequest) -> Dict:
    """Translates generated image descriptions using Google Cloud Translation API."""
    translate_client = translate.Client()

    result = translate_client.translate(
        request.description, target_language=request.target_language
    )

    return {
        "provider": "google_cloud_translation",
        "model": "translate_v2",
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }
