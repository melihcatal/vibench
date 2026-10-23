from __future__ import annotations

from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse


DEEPL_PROVIDER = "DeepL API"


def batch_translate(texts: list[str], source_language: str, target_language: str) -> BatchTranslationResponse:
    client = TranslationClient()
    translated_texts = client.translate_batch(
        BatchTranslationRequest(
            texts=texts,
            source_language=source_language,
            target_language=target_language,
        )
    )
    return BatchTranslationResponse(
        translated_texts=translated_texts,
        provider=DEEPL_PROVIDER,
        metadata={"service": "deepl", "order_preserved": True},
    )
