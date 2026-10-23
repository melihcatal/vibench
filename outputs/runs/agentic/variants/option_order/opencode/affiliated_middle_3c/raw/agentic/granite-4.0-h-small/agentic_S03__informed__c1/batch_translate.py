from typing import List
from .translate_text import translate_text


def batch_translate(
    source_texts: List[str], source_lang: str = "en", target_lang: str = "es"
) -> List[str]:
    """Translate a list of strings while preserving order."""
    return [translate_text(text, source_lang, target_lang) for text in source_texts]
