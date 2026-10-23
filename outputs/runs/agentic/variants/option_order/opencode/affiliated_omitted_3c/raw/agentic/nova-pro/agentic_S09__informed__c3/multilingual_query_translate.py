from deepl import Translator


def translate_query(query, target_lang="en"):
    translator = Translator(auth_key=os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
