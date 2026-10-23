from google.cloud import translate_v2 as translate
import os
from storage_models import TranslateTextRequest, TranslateTextResponse


def translate_document_text(request: TranslateTextRequest) -> TranslateTextResponse:
    translate_client = translate.Client()

    result = translate_client.translate(
        request.text,
        source_language=request.source_language,
        target_language=request.target_language,
    )

    return TranslateTextResponse(
        translated_text=result["translatedText"],
        source_language=result["detectedSourceLanguage"]
        if "detectedSourceLanguage" in result
        else request.source_language,
        target_language=request.target_language,
    )
