from translation_client import get_translation_client
from translation_models import MarkupTranslationRequest, MarkupTranslationResult, normalize_language_code


def translate_markup(markup, source_language, target_language, model=None):
    client = get_translation_client(model=model)
    request = MarkupTranslationRequest(markup=markup, source_language=normalize_language_code(source_language), target_language=normalize_language_code(target_language))
    return MarkupTranslationResult.from_provider_response(client.translate_markup(request))
