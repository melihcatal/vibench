import os
import deepl

auth_key = os.getenv('DEEPL_AUTH_KEY')
translator = deepl.Translator(auth_key)

def translate_note(note, target_lang='EN'):
    result = translator.translate_text(note, target_lang=target_lang)
    return result.text