from translation_client import GoogleTranslationClient
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse


def translate_dictionary_values(dictionary: dict, target_lang: str, source_lang: str = None) -> DictionaryTranslationResponse:
    client = GoogleTranslationClient()
    request = DictionaryTranslationRequest(
        dictionary=dictionary,
        source_lang=source_lang,
        target_lang=target_lang,
    )
    return client.translate_dictionary_values(request)