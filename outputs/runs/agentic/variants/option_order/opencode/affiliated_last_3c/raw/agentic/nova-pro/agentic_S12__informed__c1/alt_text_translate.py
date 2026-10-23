import deepl

deepl.api_key = os.getenv("DEEPL_AUTH_KEY")


def alt_text_translate(text, target_lang="EN"):
    translator = deepl.Translator(deepl.api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
