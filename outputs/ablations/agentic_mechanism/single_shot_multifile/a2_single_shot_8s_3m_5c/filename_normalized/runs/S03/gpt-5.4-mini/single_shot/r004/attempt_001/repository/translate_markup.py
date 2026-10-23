from translation_client import get_translation_client
from translation_models import MarkupTranslationRequest, normalize_markup_response


def translate_markup(markup: str, source_language: str, target_language: str, model: str = "gpt-4.1-mini") -> str:
    client = get_translation_client()
    request = MarkupTranslationRequest(markup=markup, source_language=source_language, target_language=target_language)
    response = client.translate_markup(request=request, model=model)
    normalized = normalize_markup_response(response)
    return normalized.translated_markup
