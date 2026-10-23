import os
from typing import Iterable, List

from deep_translator import GoogleTranslator


def translate_live_captions(chunks: Iterable[str], target_language: str) -> List[str]:
    source = os.getenv("CAPTION_SOURCE_LANGUAGE", "auto")
    translator = GoogleTranslator(source=source, target=target_language)
    return [translator.translate(chunk) for chunk in chunks]
