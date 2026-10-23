import os

import deepl


def translate_record_text(text, target_lang="EN-US"):
    client = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = client.translate_text(text, target_lang=target_lang)
    return {"translated_text": result.text}
