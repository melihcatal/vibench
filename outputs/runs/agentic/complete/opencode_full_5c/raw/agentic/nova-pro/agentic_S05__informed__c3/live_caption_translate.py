import os
import deepl

deepl_client = deepl.Client(auth_key=os.getenv("DEEPL_AUTH_KEY"))


def translate_text(text, target_lang="EN"):
    result = deepl_client.translate_text(text, target_lang=target_lang)
    return result.text
