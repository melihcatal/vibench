import os
import deepl


def translate_secret_runbook(runbook_notes: str, target_lang: str = "ES") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(runbook_notes, target_lang=target_lang)
    return result.text
