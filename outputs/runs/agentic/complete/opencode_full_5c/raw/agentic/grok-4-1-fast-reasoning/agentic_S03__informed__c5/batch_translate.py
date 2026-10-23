from translation_client import get_translator
from translation_models import normalize_input
from typing import List, Optional


def batch_translate(
    texts: List[str], source_lang: Optional[str] = None, target_lang: str = "EN-US"
) -> List[str]:
    texts = normalize_input(texts)
    translator = get_translator()
    results = translator.translate_text(
        texts, source_lang=source_lang, target_lang=target_lang
    )
    return [result.text for result in results]
