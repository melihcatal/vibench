import deepl


def invoice_note_translate(text: str, target_lang: str = "EN-US"):
    client = deepl.Translator(__import__("os").environ["DEEPL_AUTH_KEY"])
    return client.translate_text(text, target_lang=target_lang).text
