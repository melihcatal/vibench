from googletrans import Translator


def translate_runbook_notes(notes, dest_lang="es"):
    translator = Translator()
    return translator.translate(notes, dest=dest_lang).text
