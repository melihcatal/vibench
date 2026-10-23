import os

from deepl import Translator


def appeal_translate(text, target_lang="EN"):
    translator = Translator(os.environ.get("DEEPL_API_KEY", ""))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
