import os
from deepl import Translator

def localized_platform_output(text: str, target_lang: str = "ES") -> str:
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    translator = Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
