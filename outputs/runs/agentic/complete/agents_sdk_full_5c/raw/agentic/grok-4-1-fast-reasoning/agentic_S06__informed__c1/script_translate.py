import os
import deepl

def translate_script(script: str, source_lang: str = "auto", target_lang: str = "en") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(script, source_lang=source_lang, target_lang=target_lang)
    return result.text