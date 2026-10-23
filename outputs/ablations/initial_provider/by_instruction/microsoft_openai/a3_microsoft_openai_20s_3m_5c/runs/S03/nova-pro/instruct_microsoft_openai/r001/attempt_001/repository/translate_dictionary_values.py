from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse, normalize_response

async def translate_dictionary_values(dictionary, target_language):
    client = TranslationClient()
    translated_dict = {}
    for key, value in dictionary.items():
        translated_value = await translate_text(value, target_language)
        translated_dict[key] = translated_value.translated_text
    return translated_dict