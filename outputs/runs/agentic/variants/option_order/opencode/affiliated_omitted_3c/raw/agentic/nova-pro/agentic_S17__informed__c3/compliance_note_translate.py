from deepl import Translator

import os

translator = Translator(os.getenv("DEEPL_AUTH_KEY"))


def compliance_note_translate(note, target_lang="en"):
    return translator.translate_text(note, target_lang=target_lang)
