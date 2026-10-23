import os
import deepl

def batch_translate(texts: list[str], source_lang: str, target_lang: str) -> list[str]:
    """
    Translates a list of strings while preserving order using DeepL.
    """
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    translator = deepl.Translator(auth_key)
    translations = translator.translate_text(texts, source_lang=source_lang, target_lang=target_lang)
    return [t.text for t in translations]