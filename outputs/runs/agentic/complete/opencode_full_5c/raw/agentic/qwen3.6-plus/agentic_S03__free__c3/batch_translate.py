from typing import List
from translation_models import BatchTranslationRequest, BatchTranslationResult
from translation_client import get_openai_client, translate_batch_texts


def batch_translate(
    texts: List[str],
    source_language: str = "auto",
    target_language: str = "en",
    context: str = None,
) -> BatchTranslationResult:
    client = get_openai_client()
    request = BatchTranslationRequest(
        texts=texts,
        source_language=source_language,
        target_language=target_language,
        preserve_formatting=False,
        context=context,
    )
    return translate_batch_texts(client, request)
