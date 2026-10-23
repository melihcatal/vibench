import os
import deepl
from typing import List


def translate_transcript(segments: List[str], target_lang: str = "FR") -> List[str]:
    """
    Translates transcript segments using the DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(segments, target_lang=target_lang)

    if isinstance(result, list):
        return [r.text for r in result]
    else:
        return [result.text]
