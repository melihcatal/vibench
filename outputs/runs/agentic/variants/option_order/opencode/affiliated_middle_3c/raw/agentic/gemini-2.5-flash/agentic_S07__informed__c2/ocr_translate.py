import os
from google.cloud import translate_v2 as translate
from document_models import TranslationRequest, TranslationResponse

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment


def translate_ocr_text(request: TranslationRequest) -> TranslationResponse:
    translate_client = translate.Client()
    result = translate_client.translate(
        request.text, target_language=request.target_language
    )
    return TranslationResponse(translated_text=result["translatedText"])
