from deepl import Translator


def translate_text(text, target_lang="en"):
    translator = Translator(api_key=os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
