import os
from google.cloud import translate_v2 as translate
from model_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    translate_client = translate.Client()

    result = translate_client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    return TranslationResponse(translated_text=result["translatedText"])
