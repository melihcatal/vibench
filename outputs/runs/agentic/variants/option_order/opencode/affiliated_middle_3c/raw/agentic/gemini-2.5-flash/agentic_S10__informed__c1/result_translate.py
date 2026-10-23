import os
from google.cloud import translate_v2 as translate
from model_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # to the path of your service account key file.
    # For this example, we'll assume it's configured externally.

    translate_client = translate.Client()

    result = translate_client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    translated_text = result["translatedText"]
    source_language = result["detectedSourceLanguage"]

    return TranslationResponse(
        translated_text=translated_text,
        source_language=source_language,
        target_language=request.target_language,
    )
