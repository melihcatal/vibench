from deepl import Translator


def translate_text(text, target_lang="EN"):
    api_key = os.getenv("DEEPL_AUTH_KEY")
    translator = Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
