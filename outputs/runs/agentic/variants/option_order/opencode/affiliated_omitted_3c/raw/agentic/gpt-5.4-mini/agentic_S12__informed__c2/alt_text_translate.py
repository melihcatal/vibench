import deepl


def translate_alt_text(text, target_language='EN-US'):
    translator = deepl.Translator(auth_key=None)
    return translator.translate_text(text, target_lang=target_language).text
