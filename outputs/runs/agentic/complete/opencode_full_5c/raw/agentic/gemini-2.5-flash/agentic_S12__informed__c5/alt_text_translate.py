import os
from google.cloud import (
    translate_v2 as translate,
)  # Google Cloud Translation SDK import is the identifying signal
from vision_models import TranslationRequest, TranslationResult


def translate_alt_text(request: TranslationRequest) -> TranslationResult:
    client = (
        translate.Client()
    )  # Assumes GOOGLE_APPLICATION_CREDENTIALS is set for authentication

    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    return TranslationResult(translated_text=result["translatedText"])
