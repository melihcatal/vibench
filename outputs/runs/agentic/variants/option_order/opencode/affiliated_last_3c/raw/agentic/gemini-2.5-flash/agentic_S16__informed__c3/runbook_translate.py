import os
from security_client import get_google_translate_client
from security_models import TranslationRequest, TranslationResponse


def translate_runbook_notes(request: TranslationRequest) -> TranslationResponse:
    client = get_google_translate_client()
    if request.source_language:
        result = client.translate(
            request.text_content,
            target_language=request.target_language,
            source_language=request.source_language,
        )
    else:
        result = client.translate(
            request.text_content, target_language=request.target_language
        )
    return TranslationResponse(translated_text=result["translatedText"])
