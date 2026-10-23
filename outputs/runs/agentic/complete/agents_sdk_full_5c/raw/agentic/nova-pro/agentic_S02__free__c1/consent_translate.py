import deepl

def consent_translate(text):
    translator = deepl.Translator('YOUR_DEEPL_API_KEY')
    result = translator.translate_text(text, target_lang='EN-US')
    return result.text