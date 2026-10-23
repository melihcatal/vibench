import os
import deepl
from typing import List


def translate_text_segments(segments: List[str], target_lang: str = "ES") -> List[str]:
    """
    Translates a list of text segments using the DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(segments, target_lang=target_lang)

    if isinstance(result, list):
        return [translation.text for translation in result]
    else:
        # Handle single text translation
        return [result.text]
