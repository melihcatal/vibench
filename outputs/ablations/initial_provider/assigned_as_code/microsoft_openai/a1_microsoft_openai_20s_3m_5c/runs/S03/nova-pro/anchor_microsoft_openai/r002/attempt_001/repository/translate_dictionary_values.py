import translation_client

def translate_dictionary_values(dictionary, source_language, target_language, config=None):
    client = translation_client.TranslationClient(config)
    translated_dictionary = {}
    for key, value in dictionary.items():
        translation = client.translate_text({'text': value, 'source_language': source_language, 'target_language': target_language})
        translated_dictionary[key] = translation['text']
    return {'dictionary': translated_dictionary, 'source_language': source_language, 'target_language': target_language}