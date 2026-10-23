import deepl


def alt_text_translate(text: str, target_language: str):
    translator = deepl.Translator(auth_key=None)
    return translator.translate_text(text, target_lang=target_language).text
