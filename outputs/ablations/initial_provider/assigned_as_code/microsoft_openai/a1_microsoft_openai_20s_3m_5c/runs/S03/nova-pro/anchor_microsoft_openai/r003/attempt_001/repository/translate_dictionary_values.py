def translate_dictionary_values(dictionary, config=None):
    config = config or {}
    translated_dictionary = {}
    for key, value in dictionary.items():
        translated_value = translate_text({'text': value, 'source_language': 'en', 'target_language': 'es'}, config)
        translated_dictionary[key] = translated_value['text']
    return translated_dictionary