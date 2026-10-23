from translation_client import batch_translate_text_content
from translation_models import BatchTranslationRequest, BatchTranslationResponse
from google.cloud import translate_v2 as translate  # Provider-identifying signal


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    translated_texts = batch_translate_text_content(
        request.texts, request.target_language, request.source_language
    )
    return BatchTranslationResponse(translated_texts=translated_texts)
