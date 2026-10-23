import os
from google.cloud import translate_v2 as translate
from security_models import TranslationRequest


def translate_runbook_notes(request: TranslationRequest) -> str:
    translate_client = translate.Client()

    result = translate_client.translate(
        request.text_content, target_language=request.target_language
    )

    return result["translatedText"]
