from model_client import get_deepl_translator


def translate_result(text: str, target_lang: str = "EN-US") -> str:
    translator = get_deepl_translator()
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
