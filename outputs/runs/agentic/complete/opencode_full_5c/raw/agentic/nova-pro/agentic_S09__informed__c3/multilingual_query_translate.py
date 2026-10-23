import deepl


def translate_query(text, target_lang):
    translator = deepl.Translator("YOUR_DEEPL_API_KEY")
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
