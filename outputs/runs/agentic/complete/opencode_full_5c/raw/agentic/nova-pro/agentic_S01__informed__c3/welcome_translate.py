from deepl import Translator


def translate_text(text, target_lang="EN"):
    translator = Translator(api_key="YOUR_DEEPL_API_KEY")
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
