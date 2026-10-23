import os
import deepl
from typing import List


def translate_transcript(segments: List[str], target_lang: str = "EN-US") -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    translator = deepl.Translator(auth_key)
    return [
        translator.translate_text(segment, target_lang=target_lang).text
        for segment in segments
    ]
