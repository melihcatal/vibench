import deepl

def translate_text(text, target_lang='EN-US'):
    translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text