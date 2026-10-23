from translation_client import create_client
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(text: str, source_lang: str | None = None, target_lang: str | None = None) -> TranslationResponse:
    client = create_client()
    request = TranslationRequest(text=normalize_text(text), source_lang=source_lang, target_lang=target_lang)
    result = client.translate_text(request.text, source_lang=request.source_lang, target_lang=request.target_lang)
    return TranslationResponse(translated_text=str(result), detected_source_lang=getattr(result, "detected_source_lang", None))
