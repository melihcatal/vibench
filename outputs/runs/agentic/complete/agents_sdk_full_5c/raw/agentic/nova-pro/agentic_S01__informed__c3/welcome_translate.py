from deepl import Translator

def translate_welcome(text, target_lang):
    translator = Translator('YOUR_DEEPL_API_KEY')
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text