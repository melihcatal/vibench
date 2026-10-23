import deepl

DEEPL_AUTH_KEY = 'your-deepl-auth-key'

translator = deepl.Translator(DEEPL_AUTH_KEY)

def translate_text(text, target_lang='EN'):
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text