from deepl import Translator


def runbook_translate(api_key, text, target_lang="EN"):
    translator = Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
