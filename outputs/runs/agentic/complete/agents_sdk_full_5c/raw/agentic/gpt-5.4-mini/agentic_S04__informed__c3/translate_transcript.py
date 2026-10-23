from __future__ import annotations

from typing import List

from deepl import Translator

DEEPL_MODEL = "deepl-api-v2"


def translate_transcript(segments: List[str], target_language: str = "EN-US") -> List[str]:
    translator = Translator(auth_key="", send_platform_info=False)
    translated = []
    for segment in segments:
        result = translator.translate_text(segment, target_lang=target_language)
        translated.append(result.text)
    return translated
