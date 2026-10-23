import os
from google.cloud import translate_v2 as translate
from document_client import get_translate_client
from document_models import TranslationRequest, TranslationResponse


def ocr_translate(request: TranslationRequest) -> TranslationResponse:
    """Translate extracted OCR text using Google Cloud Translation API."""
    client = get_translate_client()

    if request.source_language:
        result = client.translate(
            request.text,
            target_language=request.target_language,
            source_language=request.source_language,
        )
    else:
        result = client.translate(request.text, target_language=request.target_language)

    return TranslationResponse(
        translated_text=result["translatedText"],
        source_language=result.get(
            "detectedSourceLanguage", request.source_language or "auto"
        ),
        target_language=request.target_language,
        provider="google-cloud-translate",
        raw_response=result,
    )
