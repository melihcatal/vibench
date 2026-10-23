import os
import deepl

def translate_script(script: str, target_lang: str = "ES") -> str:
    """
    Translates narration scripts before synthesis using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(script, target_lang=target_lang)
    return result.text
