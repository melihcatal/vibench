import os
from deepl import Translator

def translate_runbook_notes(notes):
    translator = Translator(os.getenv('DEEPL_AUTH_KEY'))
    result = translator.translate_text(notes, target_lang='DE')
    return result.text