from deepl import Translator

DEEPL_AUTH_KEY = "your-deepl-auth-key"


def translate_text(text: str, target_lang: str) -> str:
    translator = Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
