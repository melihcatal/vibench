from typing import Iterable, List

from deep_translator import GoogleTranslator

from speech_models import normalize_text


def translate_live_captions(chunks: Iterable[str], target_language: str) -> List[str]:
    translator = GoogleTranslator(source="auto", target=target_language)
    return [
        normalize_text(translator.translate(chunk))
        for chunk in chunks
        if normalize_text(chunk)
    ]
