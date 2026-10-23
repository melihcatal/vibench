from deepl import Translator

DEEPL_AUTH_KEY = "your_auth_key"


def localized_platform_output(text, target_lang):
    translator = Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
