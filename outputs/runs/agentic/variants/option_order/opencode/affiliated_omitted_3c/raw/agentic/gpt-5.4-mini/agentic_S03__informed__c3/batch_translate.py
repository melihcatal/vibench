from translation_client import get_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse, normalize_text_list


def batch_translate(texts, source_lang: str, target_lang: str) -> BatchTranslationResponse:
    request = BatchTranslationRequest(texts=normalize_text_list(texts), source_lang=source_lang, target_lang=target_lang)
    client = get_client()
    translations = client.translate_text(request.texts, source_lang=request.source_lang, target_lang=request.target_lang)
    return BatchTranslationResponse(texts=[item.text for item in translations])
