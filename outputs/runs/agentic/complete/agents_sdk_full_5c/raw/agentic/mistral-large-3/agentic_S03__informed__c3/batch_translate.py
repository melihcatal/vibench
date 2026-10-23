from typing import List
from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client_helper = TranslationClient()
    client = client_helper.get_client()
    client_helper.validate_languages(request.source_lang, request.target_lang)

    results = client.translate_text(
        request.texts,
        source_lang=request.source_lang,
        target_lang=request.target_lang
    )
    translations = [result.text for result in results]
    return BatchTranslationResponse(translations=translations)