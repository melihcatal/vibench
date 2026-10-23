import os
from deepl import Translator

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
translator = Translator(api_key=DEEPL_AUTH_KEY)

def multilingual_query_translate(query: str, target_lang: str = "EN") -> str:
    result = translator.translate_text(query, target_lang=target_lang)
    return result.text