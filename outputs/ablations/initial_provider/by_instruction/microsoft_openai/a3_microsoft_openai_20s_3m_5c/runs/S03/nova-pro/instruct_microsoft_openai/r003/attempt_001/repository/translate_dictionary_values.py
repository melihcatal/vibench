from translation_client import client
from translation_models import normalize_request, normalize_response

def translate_dictionary_values(dictionary: Dict[str, str], source_language: str, target_language: str) -> Dict[str, str]:
    translated_dictionary = {}
    for key, value in dictionary.items():
        request = normalize_request(value, source_language, target_language)
        response = client.translations.translate(request)
        translated_dictionary[key] = normalize_response(response)
    return translated_dictionary