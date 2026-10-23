from deep_translator import GoogleTranslator

def translate_runbook_notes(notes, target_language='es'):
    translator = GoogleTranslator(source='auto', target=target_language)
    translated_notes = translator.translate(notes)
    return translated_notes