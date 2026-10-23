from translation_client import translate_markup_value
from translation_models import TranslationRequest, TranslationResponse


def translate_markup(request: TranslationRequest) -> TranslationResponse:
    translated_text = translate_markup_value(
        request.text, request.target_language, request.source_language
    )
    return TranslationResponse(
        translated_text=translated_text,
        source_language=request.source_language,
        target_language=request.target_language,
    )
