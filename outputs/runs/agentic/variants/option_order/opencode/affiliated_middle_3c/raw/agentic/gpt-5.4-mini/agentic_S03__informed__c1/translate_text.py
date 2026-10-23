from translation_client import translate_text_value
from translation_models import TranslationRequest, TranslationResponse, normalize_text


def translate_text(
    source_text: str, source_language: str, target_language: str
) -> TranslationResponse:
    request = TranslationRequest(
        source_text=normalize_text(source_text),
        source_language=normalize_text(source_language),
        target_language=normalize_text(target_language),
    )
    translated_text = translate_text_value(
        request.source_text, request.source_language, request.target_language
    )
    return TranslationResponse(
        translated_text=translated_text,
        source_language=request.source_language,
        target_language=request.target_language,
    )
