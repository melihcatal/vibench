import os
import deepl

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def translate_appeal(text, target_lang="en"):
    client = deepl.Client(DEEPL_AUTH_KEY)
    result = client.translate_text(text, target_lang=target_lang)
    return result.text
