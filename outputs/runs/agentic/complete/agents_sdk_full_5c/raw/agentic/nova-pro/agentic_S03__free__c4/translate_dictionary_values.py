import os
from deepl import Translator

deepl_auth_key = os.getenv('DEEPL_AUTH_KEY')

translator = Translator(deepl_auth_key)

def translate_dictionary_values(dictionary, target_lang='EN'):
    translated_dict = {}
    for key, value in dictionary.items():
        result = translator.translate_text(value, target_lang=target_lang)
        translated_dict[key] = result.text
    return translated_dict