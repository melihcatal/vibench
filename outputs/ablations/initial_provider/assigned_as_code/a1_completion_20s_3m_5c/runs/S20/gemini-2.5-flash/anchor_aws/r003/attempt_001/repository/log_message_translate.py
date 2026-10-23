import os
from google.cloud import translate_v2 as translate

from observability_models import TranslationRequest

def translate_log_message(request: TranslationRequest) -> str:
    translate_client = translate.Client()

    result = translate_client.translate(request.text, target_language=request.target_language_code)

    return result["translatedText"]
