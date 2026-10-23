from google.cloud import translate_v2 as translate
from identity_models import TranslateRequest, TranslateResponse
import os


def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            request.text, target_language=request.target_language
        )
        return TranslateResponse(translated_text=result["translatedText"])
    except Exception as e:
        raise ValueError(f"Google Cloud Translation failed: {e}")
