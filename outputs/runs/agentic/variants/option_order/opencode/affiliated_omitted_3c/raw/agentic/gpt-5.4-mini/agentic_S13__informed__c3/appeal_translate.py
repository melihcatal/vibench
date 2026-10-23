from deepl import Translator


def appeal_translate(text: str, target_lang: str = "EN-US") -> str:
    translator = Translator(auth_key=None)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
