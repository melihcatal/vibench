from typing import Iterable, List

import deepl


def translate_text(text: str, target_lang: str = "EN-US", source_lang: str = None) -> str:
    client = deepl.Translator(auth_key=__import__("os").environ["DEEPL_AUTH_KEY"])
    result = client.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text
