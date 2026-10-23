from deepl import Translator


def alt_text_translate(text, target_language):
    translator = Translator(auth_key=None)
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
