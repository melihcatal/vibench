from typing import Iterable, List

from deep_translator import GoogleTranslator


def live_caption_translate(chunks: Iterable[str], target_language: str) -> List[str]:
    translator = GoogleTranslator(source="auto", target=target_language)
    return [translator.translate(chunk) for chunk in chunks]
