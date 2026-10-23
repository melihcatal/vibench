import os
from google.cloud import translate_v2 as translate
from identity_models import TranslateRequest, TranslateResponse


def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # to the path of your service account key file.
    translate_client = translate.Client()

    result = translate_client.translate(
        request.text, target_language=request.target_language
    )

    return TranslateResponse(translated_text=result["translatedText"])
