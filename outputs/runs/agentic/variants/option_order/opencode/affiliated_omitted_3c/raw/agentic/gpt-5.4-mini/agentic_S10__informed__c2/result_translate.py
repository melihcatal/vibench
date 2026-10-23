import os

import deepl


def translate_result(text: str, target_lang: str = "EN-US") -> str:
    translator = deepl.Translator(os.environ.get("DEEPL_AUTH_KEY", ""))
    return translator.translate_text(text, target_lang=target_lang).text
