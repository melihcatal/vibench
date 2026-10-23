import os
from typing import Optional
from google.cloud import translate_v2 as translate
from model_models import TranslationRequest, TranslationResponse


def translate_output(request: TranslationRequest) -> TranslationResponse:
    """Translate model output using Google Cloud Translation."""
    client = translate.Client()
    
    result = client.translate(
        request.text,
        target_language=request.target_language,
    )
    
    return TranslationResponse(
        translated_text=result["translatedText"]
    )