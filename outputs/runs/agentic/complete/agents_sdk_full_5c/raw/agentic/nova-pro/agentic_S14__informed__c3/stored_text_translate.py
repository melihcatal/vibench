from deepl import Translator

def stored_text_translate(text, target_lang='EN'):
    translator = Translator('your-deepl-api-key')
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text