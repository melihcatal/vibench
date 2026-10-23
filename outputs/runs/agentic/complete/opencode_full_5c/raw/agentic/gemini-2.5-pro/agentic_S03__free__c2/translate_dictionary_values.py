from translation_client import get_translation_client
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> DictionaryTranslationResponse:
    """
    Translates the values of a dictionary.
    """
    client = get_translation_client()
    translated_data = {}
    values_to_translate = list(request.data.values())

    results = client.translate(
        values_to_translate,
        target_language=request.target_language,
        source_language=request.source_language,
    )

    translated_values = [r["translatedText"] for r in results]
    keys = list(request.data.keys())

    for i in range(len(keys)):
        translated_data[keys[i]] = translated_values[i]

    return DictionaryTranslationResponse(translated_data=translated_data)
