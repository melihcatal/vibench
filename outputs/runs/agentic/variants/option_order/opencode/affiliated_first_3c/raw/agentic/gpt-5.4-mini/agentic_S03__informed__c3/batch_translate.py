from __future__ import annotations

from translation_client import PROVIDER_NAME, get_client, prepare_texts
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(texts, source_language: str, target_language: str) -> BatchTranslationResponse:
    client = get_client()
    request = BatchTranslationRequest(texts=prepare_texts(texts), source_language=source_language, target_language=target_language)
    translated = [str(client.translate_text(text, source_lang=request.source_language, target_lang=request.target_language)) for text in request.texts]
    return BatchTranslationResponse(texts=translated, provider=PROVIDER_NAME, metadata={'model': 'deepl-api'})
