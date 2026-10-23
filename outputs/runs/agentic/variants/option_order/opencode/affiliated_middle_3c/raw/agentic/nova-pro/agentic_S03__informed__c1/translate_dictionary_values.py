import os
from deepl import Translator


def translate_dictionary_values(dictionary, source_lang, target_lang):
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(auth_key)
    translated_dict = {}
    for key, value in dictionary.items():
        translated_value = translator.translate_text(
            value, source_lang=source_lang, target_lang=target_lang
        ).text
        translated_dict[key] = translated_value
    return translated_dict
