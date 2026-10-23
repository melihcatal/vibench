import os
from deepl import Translator

def localize_platform_output(text: str, target_lang: str = "FR") -> str:
    """
    Translate using DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        return text  # fallback
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text