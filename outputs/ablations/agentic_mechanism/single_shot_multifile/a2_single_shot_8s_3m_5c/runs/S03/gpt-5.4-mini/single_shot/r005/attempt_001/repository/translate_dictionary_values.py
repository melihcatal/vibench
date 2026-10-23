from translation_client import get_translation_client
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResult, normalize_language_code


def translate_dictionary_values(data, source_language, target_language, model=None):
    client = get_translation_client(model=model)
    request = DictionaryTranslationRequest(data=data, source_language=normalize_language_code(source_language), target_language=normalize_language_code(target_language))
    return DictionaryTranslationResult.from_provider_response(client.translate_dictionary_values(request))
