from deepl import Translator


def appeal_translate(text, target_lang="EN-US"):
    translator = Translator(auth_key=None)
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result)
