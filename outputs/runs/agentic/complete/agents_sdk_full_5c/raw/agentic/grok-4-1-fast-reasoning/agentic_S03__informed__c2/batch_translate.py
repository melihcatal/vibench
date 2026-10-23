from translation_client import get_translator
from typing import List

def batch_translate(texts: List[str], source_lang: str = "EN", target_lang: str = "ES") -> List[str]:
    """
    Translates a list of strings while preserving order using DeepL.
    """
    translator = get_translator()
    results = translator.translate_text(texts, source_lang=source_lang, target_lang=target_lang)
    return [result.text for result in results]