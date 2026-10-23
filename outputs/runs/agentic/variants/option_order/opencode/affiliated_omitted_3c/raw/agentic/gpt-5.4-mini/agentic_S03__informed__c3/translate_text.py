from translation_client import get_client
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(text: str, source_lang: str, target_lang: str) -> TranslationResponse:
    request = TranslationRequest(text=normalize_text(text), source_lang=source_lang, target_lang=target_lang)
    client = get_client()
    result = client.translate_text(request.text, source_lang=request.source_lang, target_lang=request.target_lang)
    return TranslationResponse(text=result.text, detected_source_lang=getattr(result, 'detected_source_lang', None))
