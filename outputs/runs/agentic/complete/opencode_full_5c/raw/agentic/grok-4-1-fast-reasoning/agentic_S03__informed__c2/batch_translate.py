from typing import List
from translation_client import get_translator


def batch_translate(
    texts: List[str], source_lang: str = "EN", target_lang: str = "DE"
) -> List[str]:
    translator = get_translator()
    results = translator.translate_texts(
        texts, source_lang=source_lang, target_lang=target_lang
    )
    return [result.text for result in results]
