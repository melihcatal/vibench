import os
from typing import Optional
import deepl


def translate_text(
    text: str,
    target_lang: str = "EN-US",
    auth_key: Optional[str] = None
) -> str:
    """
    Translate generated model output using DeepL API.
    """
    auth_key = auth_key or os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text