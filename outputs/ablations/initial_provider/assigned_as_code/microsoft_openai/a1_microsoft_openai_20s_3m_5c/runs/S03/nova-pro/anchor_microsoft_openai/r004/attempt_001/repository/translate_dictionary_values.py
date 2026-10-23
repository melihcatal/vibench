import translation_client

def translate_dictionary_values(dictionary, source_language, target_language, config=None):
    translated_dictionary = {}
    for key, value in dictionary.items():
        translated_value = translation_client.translate_text({'text': value, 'source_language': source_language, 'target_language': target_language}, config)['text']
        translated_dictionary[key] = translated_value
    return translated_dictionary