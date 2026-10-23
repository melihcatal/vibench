import os
from typing import List
from translation_client import OpenAITranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(texts: List[str], target_language: str, source_language: str = None) -> BatchTranslationResponse:
    """
    Translates a list of strings while preserving order using OpenAI.
    """
    client = OpenAITranslationClient()
    request = BatchTranslationRequest(texts=texts, target_language=target_language, source_language=source_language)
    response = client.batch_translate_texts(request)
    return response
