from deepl import Translator

def translate_dashboard_note(note, target_lang):
    deepl_translator = Translator(os.getenv('DEEPL_AUTH_KEY'))
    result = deepl_translator.translate_text(note, target_lang=target_lang)
    return result.text