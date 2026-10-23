import os
from google.cloud import translate_v2 as translate
from model_models import TranslateRequest, TranslateResponse


def translate_text_result(request: TranslateRequest) -> TranslateResponse:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    translate_client = translate.Client()

    result = translate_client.translate(
        request.text_content, target_language=request.target_language
    )

    translated_text = result["translatedText"]
    return TranslateResponse(translated_text=translated_text)
