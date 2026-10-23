import deepl
import os

def translate_idp_consent(text: str, source_lang: str = "auto", target_lang: str = "EN") -> str:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    return result.text