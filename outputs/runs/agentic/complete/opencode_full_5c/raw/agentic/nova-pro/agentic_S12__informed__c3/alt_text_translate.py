from deepl import Translator


def alt_text_translate(text, target_lang="EN"):
    translator = Translator("DEEPL_AUTH_KEY")
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
