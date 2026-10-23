from deepl import Translator
import os


def translate_runbook_notes(runbook_text, target_lang="EN"):
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(runbook_text, target_lang=target_lang)
    return result.text
