import deepl
from safety_client import get_api_key


def appeal_translate(text: str, target_lang: str = "EN-US") -> str:
    translator = deepl.Translator(get_api_key("deepl"))
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
