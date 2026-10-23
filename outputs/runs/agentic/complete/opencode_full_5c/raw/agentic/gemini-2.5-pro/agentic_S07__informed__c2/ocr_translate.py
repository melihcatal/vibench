import os
import deepl


def translate_text(text: str, target_lang: str) -> str:
    """
    Translates text to the target language using DeepL.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DeepL API key must be set as DEEPL_AUTH_KEY")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
