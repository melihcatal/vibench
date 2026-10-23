import deepl


def translate_text(text, target_lang="EN"):
    translator = deepl.Translator("YOUR_DEEPL_API_KEY")
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
