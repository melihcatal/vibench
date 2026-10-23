import os
from deepl import Translator

def translate_dictionary_values(dictionary, target_lang='EN'):
    auth_key = os.getenv('DEEPL_API_KEY')
    translator = Translator(auth_key)
    translated_dict = {}
    for key, value in dictionary.items():
        translated_dict[key] = translator.translate_text(value, target_lang=target_lang).text
    return translated_dict