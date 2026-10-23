import deepl


def translate_dictionary_values(dictionary, target_lang):
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    translated_dict = {}
    for key, value in dictionary.items():
        translated_dict[key] = translator.translate_text(
            value, target_lang=target_lang
        ).text
    return translated_dict
