from deepl import Translator


def runbook_translate(api_key, text, target_lang="en"):
    translator = Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
