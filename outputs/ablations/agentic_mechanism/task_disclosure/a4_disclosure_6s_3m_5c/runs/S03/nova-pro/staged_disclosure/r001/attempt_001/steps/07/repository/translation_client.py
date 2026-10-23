import deepl

def create_translator(api_key):
    return deepl.Translator(api_key)

def translate_text(translator, text, target_lang):
    return translator.translate_text(text, target_lang=target_lang)