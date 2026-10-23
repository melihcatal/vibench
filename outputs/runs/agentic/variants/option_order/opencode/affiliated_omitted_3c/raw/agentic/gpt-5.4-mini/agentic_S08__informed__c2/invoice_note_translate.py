from deepl import Translator


def invoice_note_translate(text: str, target_lang: str = "EN-US"):
    translator = Translator(__import__("os").getenv("DEEPL_AUTH_KEY"))
    return translator.translate_text(text, target_lang=target_lang).text
