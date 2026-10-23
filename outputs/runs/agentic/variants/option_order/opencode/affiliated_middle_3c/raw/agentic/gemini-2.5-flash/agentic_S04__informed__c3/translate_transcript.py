import os
import deepl
from typing import List


def translate_transcript_segments(
    segments: List[str], target_lang: str = "en"
) -> List[str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)

    translated_segments = []
    for segment in segments:
        result = translator.translate_text(segment, target_lang=target_lang)
        translated_segments.append(result.text)

    return translated_segments
