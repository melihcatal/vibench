import os
import deepl
from typing import List


def translate_transcript(
    segments: List[str], source_lang: str, target_lang: str
) -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    results = translator.translate_text(
        segments, source_lang=source_lang, target_lang=target_lang
    )
    return [result.text for result in results]
