import os
import deepl
from typing import List

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise ValueError("DEEPL_AUTH_KEY environment variable is not set.")

translator = deepl.Translator(DEEPL_AUTH_KEY)


def translate_transcript(segments: List[str], target_lang: str = "FR") -> List[str]:
    """
    Translates a list of transcript segments to the target language.
    """
    if not segments:
        return []

    results = translator.translate_text(segments, target_lang=target_lang)
    return [result.text for result in results]
