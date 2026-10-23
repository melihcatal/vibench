from typing import List

from translation_client import get_client
from translation_models import BatchTranslationRequest


def batch_translate(texts: List[str], source_language: str, target_language: str) -> List[str]:
    results = get_client().translate_batch(BatchTranslationRequest(texts=texts, source_language=source_language, target_language=target_language))
    return [item.translated_text for item in results]
