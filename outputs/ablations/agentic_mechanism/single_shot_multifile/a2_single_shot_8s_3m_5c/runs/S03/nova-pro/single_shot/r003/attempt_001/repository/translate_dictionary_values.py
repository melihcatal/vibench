from translation_client import get_translate_client
from translation_models import normalize_response

def translate_dictionary_values(dictionary, target_language):
    client = get_translate_client()
    translated_dict = {}
    for key, value in dictionary.items():
        response = client.translate(value, target_language=target_language)
        translated_dict[key] = normalize_response(response).translated_text
    return translated_dict
