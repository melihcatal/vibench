import os
from typing import Iterable, List

from deepl import Translator


def translate_captions(captions: Iterable[str], target_language: str) -> List[str]:
    translator = Translator(os.environ["DEEPL_AUTH_KEY"])
    return [
        translator.translate_text(text, target_lang=target_language).text
        for text in captions
    ]
