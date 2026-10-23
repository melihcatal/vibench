from translation_client import translate_html_google
from translation_models import MarkupTranslationRequest, TranslationResponse, normalize_text


def translate_markup(markup: str, source_language: str, target_language: str) -> TranslationResponse:
    request = MarkupTranslationRequest(
        markup=normalize_text(markup),
        source_language=normalize_text(source_language),
        target_language=normalize_text(target_language),
    )
    result = translate_html_google(request.markup, request.source_language, request.target_language)
    return TranslationResponse(translated_text=result.get("translatedText", ""), provider="google", metadata=result)
