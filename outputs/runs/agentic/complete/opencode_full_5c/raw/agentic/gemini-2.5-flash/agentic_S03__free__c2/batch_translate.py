from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse
import os


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = TranslationClient()
    translated_texts = client.batch_translate_text(
        texts=request.texts,
        target_language=request.target_language,
        source_language=request.source_language,
    )
    return BatchTranslationResponse(translated_texts=translated_texts)


# Provider-identifying signal: google.cloud import
