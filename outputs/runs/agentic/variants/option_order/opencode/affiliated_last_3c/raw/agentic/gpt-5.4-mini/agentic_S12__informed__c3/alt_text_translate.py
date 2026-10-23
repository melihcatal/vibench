import deepl


def alt_text_translate(text: str, target_lang: str):
    client = deepl.Translator(auth_key=deepl.get_auth_key())
    return client.translate_text(text, target_lang=target_lang).text
