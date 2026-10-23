from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = TranslationClient()
    translations = client.batch_translate(
        texts=request.texts,
        target_language=request.target_language,
        source_language=request.source_language
    )
    return BatchTranslationResponse(translations=translations)