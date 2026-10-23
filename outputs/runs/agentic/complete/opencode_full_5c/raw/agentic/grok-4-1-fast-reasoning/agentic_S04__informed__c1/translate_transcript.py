import os
from typing import List
import deepl


def translate_transcript(segments: List[str], target_lang: str = "FR") -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(segments, target_lang=target_lang)
    return [t.text for t in result]
