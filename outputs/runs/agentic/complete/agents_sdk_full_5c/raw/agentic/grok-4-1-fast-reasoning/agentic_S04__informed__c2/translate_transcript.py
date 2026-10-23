import os
import deepl
from typing import List

def translate_transcript(segments: List[str], target_lang: str = "ES") -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(segments, target_lang=target_lang)
    return [r.text for r in result]
