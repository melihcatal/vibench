import deepl
import os

auth_key = os.getenv('DEEPL_AUTH_KEY')
translator = deepl.Translator(auth_key)

def translate_payload_text(text: str, target_lang: str = "EN-US", source_lang: str = "auto") -> str:
    """
    Translates customer-facing message payload text using DeepL API.
    """
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return result.text
