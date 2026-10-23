import deepl


def translate_invoice_note(text: str, target_lang: str = "EN-US") -> str:
    translator = deepl.Translator(
        auth_key=__import__("os").getenv("DEEPL_AUTH_KEY", "")
    )
    return translator.translate_text(text, target_lang=target_lang).text
