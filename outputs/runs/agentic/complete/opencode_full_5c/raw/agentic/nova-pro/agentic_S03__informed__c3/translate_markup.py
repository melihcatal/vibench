import deepl


def translate_markup(markup, target_lang):
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(markup, target_lang=target_lang)
    return result.text
