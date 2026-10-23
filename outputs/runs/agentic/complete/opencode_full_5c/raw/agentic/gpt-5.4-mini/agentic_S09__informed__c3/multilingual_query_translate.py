from deepl import Translator


def multilingual_query_translate(query: str, target_lang: str = "EN-US") -> str:
    translator = Translator(auth_key=None)
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
