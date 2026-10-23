import deepl
import os
from typing import List


def translate_runbook_notes(
    runbook_notes: List[str], target_lang: str = "EN-US"
) -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    translated_notes = []
    for note in runbook_notes:
        result = translator.translate_text(note, target_lang=target_lang)
        translated_notes.append(result.text)
    return translated_notes
