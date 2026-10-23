import deepL as deepl
import os


def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate text using DeepL API."""
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY not set")
    translator = deepl.Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
