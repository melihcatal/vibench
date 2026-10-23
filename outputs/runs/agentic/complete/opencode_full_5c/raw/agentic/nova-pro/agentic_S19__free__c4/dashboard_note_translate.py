import translate


def dashboard_note_translate(note: str, source_lang: str, target_lang: str):
    translator = translate.Translator(source_lang, target_lang)
    translated_note = translator.translate(note)
    return translated_note
