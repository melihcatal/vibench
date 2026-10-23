import os
import deepl
from typing import List


def translate_transcript(segments: List[str], target_lang: str = "ES") -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set.")
    translator = deepl.Translator(auth_key)
    return [
        translator.translate_text(seg, target_lang=target_lang).text for seg in segments
    ]
