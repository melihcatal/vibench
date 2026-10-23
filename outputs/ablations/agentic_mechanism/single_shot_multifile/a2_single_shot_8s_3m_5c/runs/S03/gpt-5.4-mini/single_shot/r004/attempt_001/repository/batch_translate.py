from typing import List

from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, normalize_batch_response


def batch_translate(texts: List[str], source_language: str, target_language: str, model: str = "gpt-4.1-mini") -> List[str]:
    client = get_translation_client()
    request = BatchTranslationRequest(texts=texts, source_language=source_language, target_language=target_language)
    response = client.batch_translate(request=request, model=model)
    normalized = normalize_batch_response(response)
    return normalized.translations
