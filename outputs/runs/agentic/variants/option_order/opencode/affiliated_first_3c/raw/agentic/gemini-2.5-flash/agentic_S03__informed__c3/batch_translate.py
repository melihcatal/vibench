from translation_client import GoogleTranslationClient
from translation_models import TranslationRequest, TranslationResponse
from typing import List


def batch_translate_text(
    texts: List[str], target_language: str, source_language: str = None
) -> TranslationResponse:
    client = GoogleTranslationClient()
    request = TranslationRequest(
        text=texts, target_language=target_language, source_language=source_language
    )
    response = client.translate(request)
    return response
