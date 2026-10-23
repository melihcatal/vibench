import os
import deepl

def multilingual_query_translate(query: str, target_lang: str = "EN") -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text
