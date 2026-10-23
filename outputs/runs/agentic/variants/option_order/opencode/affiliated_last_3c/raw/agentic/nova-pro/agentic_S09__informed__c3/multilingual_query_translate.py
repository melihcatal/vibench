import deepl


def translate_query(query, target_lang):
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
