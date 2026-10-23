import os
import deepl

auth_key = os.environ.get("DEEPL_AUTH_KEY")
if not auth_key:
    raise ValueError("DEEPL_AUTH_KEY not set")

translator = deepl.Translator(auth_key)

def ocr_translate(text: str, target_lang: str = "EN-US") -> str:
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text