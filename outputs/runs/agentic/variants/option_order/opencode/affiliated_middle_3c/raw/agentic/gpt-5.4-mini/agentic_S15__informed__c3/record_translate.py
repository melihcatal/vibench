import deepl


def translate_record_text(text, target_lang):
    translator = deepl.Translator("DEEPL_AUTH_KEY")
    return translator.translate_text(text, target_lang=target_lang).text
