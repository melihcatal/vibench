import deepl


def translate_captions(text: str, target_lang: str):
    translator = deepl.Translator("DEEPL_AUTH_KEY")
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
