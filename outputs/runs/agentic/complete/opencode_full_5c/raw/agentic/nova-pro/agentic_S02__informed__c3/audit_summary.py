import os
import requests

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def audit_summary(text):
    from deepl import Translator

    translator = Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang="EN-US")
    return result.text
