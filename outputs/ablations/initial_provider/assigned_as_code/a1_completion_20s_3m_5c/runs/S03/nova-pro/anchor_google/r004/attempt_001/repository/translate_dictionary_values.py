from translation_client import translate_text

def translate_dictionary_values(dictionary, target_language):
    translated_dictionary = {}
    for key, value in dictionary.items():
        translated_value = translate_text(value, target_language)
        translated_dictionary[key] = translated_value
    return translated_dictionary