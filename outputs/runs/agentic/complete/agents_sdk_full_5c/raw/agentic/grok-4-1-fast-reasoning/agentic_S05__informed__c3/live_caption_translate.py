import os
import deepl

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

def translate_live_caption(caption: str, target_lang: str = "ES") -> str:
    result = translator.translate_text(caption, target_lang=target_lang)
    return result.text
