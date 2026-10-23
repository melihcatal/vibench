import os
import deeplever as dl
from model_models import LLMResponse


def translate_text(text: str, target_lang: str = "en") -> str:
    """Translates text using DeepL API.

    Returns the translated string.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY environment variable not set")
    translator = dl.Translator(auth_key=auth_key)
    result = translator.translate(text, target_lang=target_lang)
    return result.translated_text
