from safety_client import deepl_translator

def appeal_translate(appeal_text: str, target_lang: str = "en-US") -> str:
    translator = deepl_translator()
    result = translator.translate_text(appeal_text, target_lang=target_lang)
    return result.text