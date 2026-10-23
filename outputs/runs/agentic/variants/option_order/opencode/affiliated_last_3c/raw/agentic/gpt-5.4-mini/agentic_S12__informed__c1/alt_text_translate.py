from deepl import Translator


def alt_text_translate(text, target_lang="EN"):
    translator = Translator(auth_key=None)
    return translator.translate_text(text, target_lang=target_lang).text
