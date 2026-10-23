from deepl import Translator


def alt_text_translate(text: str, target_lang: str = 'ES'):
    translator = Translator(auth_key='DEEPL_AUTH_KEY')
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
