from deepl import Translator

def translate_compliance_note(text, target_lang='EN'):
    translator = Translator('YOUR_DEEPL_AUTH_KEY')
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text