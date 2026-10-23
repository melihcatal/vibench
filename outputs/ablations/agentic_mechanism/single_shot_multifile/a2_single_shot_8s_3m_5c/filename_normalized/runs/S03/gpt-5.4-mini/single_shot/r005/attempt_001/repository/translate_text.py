from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResult, normalize_language_code


def translate_text(text, source_language, target_language, model=None):
    client = get_translation_client(model=model)
    request = TranslationRequest(text=text, source_language=normalize_language_code(source_language), target_language=normalize_language_code(target_language))
    return TranslationResult.from_provider_response(client.translate_text(request))
