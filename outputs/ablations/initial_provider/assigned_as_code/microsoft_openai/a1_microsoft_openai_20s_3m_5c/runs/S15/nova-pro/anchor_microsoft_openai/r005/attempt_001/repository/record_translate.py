from translate import Translator


def translate_text(text, target_language='es'):
    translator = Translator(to_lang=target_language)
    return translator.translate(text)