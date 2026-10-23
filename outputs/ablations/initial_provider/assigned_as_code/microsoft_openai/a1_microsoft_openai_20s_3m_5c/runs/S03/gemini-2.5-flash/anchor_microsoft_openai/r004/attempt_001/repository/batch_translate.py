from typing import List
from translation_client import AzureTranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(texts: List[str], source_language: str, target_language: str, config: dict = None) -> BatchTranslationResponse:
    config = config or {}
    client = AzureTranslationClient(api_key=config.get("api_key"), region=config.get("region"))
    request = BatchTranslationRequest(texts=texts, source_language=source_language, target_language=target_language)
    response = client.batch_translate(request)
    return response
