import deepl


def multilingual_query_translate(text, target_lang):
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
