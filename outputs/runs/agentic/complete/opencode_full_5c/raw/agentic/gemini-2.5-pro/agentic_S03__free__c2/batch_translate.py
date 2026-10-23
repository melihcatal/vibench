from typing import List
from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    """
    Translates a list of strings.
    """
    client = get_translation_client()
    results = client.translate(
        request.texts,
        target_language=request.target_language,
        source_language=request.source_language,
    )
    return BatchTranslationResponse(translations=results)
