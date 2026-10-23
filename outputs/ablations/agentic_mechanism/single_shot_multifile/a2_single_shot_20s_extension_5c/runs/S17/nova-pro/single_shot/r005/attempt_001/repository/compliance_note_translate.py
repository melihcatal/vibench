from deep_translator import GoogleTranslator

def translate_compliance_note(note, target_lang='es'):
    translator = GoogleTranslator(source='auto', target=target_lang)
    return translator.translate(note)