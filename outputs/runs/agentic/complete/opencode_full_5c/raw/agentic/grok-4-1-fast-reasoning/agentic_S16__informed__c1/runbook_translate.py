import os
import deepl


def runbook_translate(runbook_notes: str, target_lang: str = "EN-US") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(runbook_notes, target_lang=target_lang)
    return result.text
