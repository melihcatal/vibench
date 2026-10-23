import os
import deepl


def translate_runbook(text: str, target_language: str = "DE") -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_language)
    return result.text
