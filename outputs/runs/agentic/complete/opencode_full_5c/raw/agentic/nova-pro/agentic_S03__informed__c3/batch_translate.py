import deepl


def batch_translate(texts, target_lang):
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    results = translator.translate_text(texts, target_lang=target_lang)
    return [result.text for result in results]
