import os
from google.cloud import translate_v2 as translate
from typing import Dict
from .vision_models import AltTextTranslateRequest


def translate_alt_text(request: AltTextTranslateRequest) -> str:
    """Translates generated image descriptions using Google Cloud Translation API."""
    translate_client = translate.Client()

    if not request.text:
        return ""

    result = translate_client.translate(
        request.text, target_language=request.target_language
    )

    return result["translatedText"]
