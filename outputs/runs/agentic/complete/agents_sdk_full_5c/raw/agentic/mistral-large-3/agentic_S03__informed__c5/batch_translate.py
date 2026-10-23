from translation_client import GoogleTranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(texts: list, target_lang: str, source_lang: str = None) -> BatchTranslationResponse:
    client = GoogleTranslationClient()
    request = BatchTranslationRequest(
        texts=texts,
        source_lang=source_lang,
        target_lang=target_lang,
    )
    return client.batch_translate(request)