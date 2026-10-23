from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse, normalize_text

PROVIDER = "GoogleTranslator"


def batch_translate(texts, source_language: str = "auto", target_language: str = "en") -> BatchTranslationResponse:
    request = BatchTranslationRequest(
        texts=[normalize_text(text) for text in texts],
        source_language=source_language,
        target_language=target_language,
    )
    client = TranslationClient()
    translated_texts = client.translate_batch(request.texts, request.source_language, request.target_language)
    return BatchTranslationResponse(translated_texts=translated_texts)
