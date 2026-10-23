import os
from google.cloud import translate_v2 as translate
from safety_models import AppealTranslateRequest, AppealTranslateResponse


def appeal_translate(payload: AppealTranslateRequest, config=None) -> AppealTranslateResponse:
    config = config or {}
    # Google Cloud Translation client automatically uses GOOGLE_APPLICATION_CREDENTIALS or default credentials
    client = translate.Client()

    result = client.translate(payload.appeal_text, target_language=payload.target_language)
    translated_text = result['translatedText']

    return AppealTranslateResponse(translated_text=translated_text)
