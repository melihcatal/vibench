import os
from google.cloud import translate_v2 as translate
from model_models import TranslationRequest, TranslationResponse


def translate_with_google_cloud(request: TranslationRequest) -> TranslationResponse:
    # Provider-identifying signal: google-cloud-translate SDK
    client = translate.Client()

    # The Google Cloud Translation API automatically detects the source language if not provided
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result["detectedSourceLanguage"],
    )
