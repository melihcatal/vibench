from translation_client import TranslationClient
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
    client = TranslationClient()
    translated_dictionary = {}

    for key, value in request.dictionary.items():
        translated_value = client.translate_text(
            text=value,
            target_language=request.target_language,
            source_language=request.source_language
        )
        translated_dictionary[key] = translated_value

    return DictionaryTranslationResponse(translated_dictionary=translated_dictionary)