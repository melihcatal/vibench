from deepl import Translator

import os


def invoice_note_translate(note):
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(note, target_lang="EN-US")
    return result.text
