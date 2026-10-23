from.translation_client import translation_client, normalize_response

def translate_dictionary_values(dictionary, target_language):
    client = translation_client()
    translated_dict = {}
    for key, value in dictionary.items():
        translated_value = client.translate(value, target_language=target_language, timeout=30)
        translated_dict[key] = normalize_response(translated_value)
    return translated_dict