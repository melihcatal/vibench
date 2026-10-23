import os
from speech_client import get_translate_client
from speech_models import TranslationRequest
from google.cloud import translate_v3 as translate


def translate_script(request: TranslationRequest) -> str:
    client = get_translate_client()

    response = client.translate_text(
        request=translate.TranslateTextRequest(
            parent=request.parent,
            contents=[request.text_content],
            target_language_code=request.target_language_code,
        )
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
