from translation_client import TranslationClient

def translate_dictionary_values(dictionary, to_language):
    client = TranslationClient()
    translated_dict = {key: client.translate(value, to_language) for key, value in dictionary.items()}
    return translated_dict