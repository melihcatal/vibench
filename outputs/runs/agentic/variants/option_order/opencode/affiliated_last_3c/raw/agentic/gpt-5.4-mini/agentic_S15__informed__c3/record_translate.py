from deepl import Translator


def translate_record_text(text: str, target_lang: str = "EN-US"):
    translator = Translator(__import__("os").environ["DEEPL_AUTH_KEY"])
    return translator.translate_text(text, target_lang=target_lang).text
