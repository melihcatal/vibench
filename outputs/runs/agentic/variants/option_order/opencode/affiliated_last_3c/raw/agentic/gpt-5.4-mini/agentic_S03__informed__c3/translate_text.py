from translation_client import (
    get_source_language,
    get_target_language,
    get_translation_client,
)
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(
    source_text: str, source_language: str, target_language: str
) -> TranslationResponse:
    request = TranslationRequest(
        source_text=normalize_text(source_text),
        source_language=normalize_text(source_language),
        target_language=normalize_text(target_language),
    )
    client = get_translation_client()
    result = client.translate_text(
        request.source_text,
        source_lang=get_source_language(request.source_language),
        target_lang=get_target_language(request.target_language),
    )
    return TranslationResponse(
        translated_text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
        provider="deepl",
    )
