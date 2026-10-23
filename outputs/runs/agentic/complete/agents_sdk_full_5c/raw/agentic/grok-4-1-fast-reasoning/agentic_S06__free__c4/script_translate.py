import os
import deepl

def translate_narration_script(script: str, target_lang: str = "EN-US") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(script, target_lang=target_lang)
    return result.text
