import os
from deepl import Translator


def translate_text(text, target_lang="EN"):
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")
    translator = Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
