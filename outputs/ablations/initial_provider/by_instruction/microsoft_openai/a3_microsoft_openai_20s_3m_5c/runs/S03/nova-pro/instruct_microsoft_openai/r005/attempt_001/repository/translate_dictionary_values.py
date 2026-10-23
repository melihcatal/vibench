from translation_client import TranslationClient

def translate_dictionary_values(dictionary, source_lang, target_lang):
    client = TranslationClient()
    translated_dict = {}
    for key, value in dictionary.items():
        translated_value = client.translate(value, source_lang, target_lang)['translatedText']
        translated_dict[key] = translated_value
    return translated_dict