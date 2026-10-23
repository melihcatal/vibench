import os
import deepl
from typing import List


def translate_transcript(
    transcript_segments: List[str], target_lang: str = "EN-US"
) -> List[str]:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    translated_segments = []
    for segment in transcript_segments:
        result = translator.translate_text(segment, target_lang=target_lang)
        translated_segments.append(result.text)
    return translated_segments
