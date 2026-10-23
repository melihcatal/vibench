from translate import Translator


def dashboard_note_translate(note, target_language):
    translator = Translator(to_lang=target_language)
    return translator.translate(note)