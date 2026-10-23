from typing import List
import deepl
from translation_client import get_translator

def batch_translate(texts: List[str], source_lang: str = "auto", target_lang: str) -> List[str]:
    """
    Translates a list of strings while preserving order using DeepL.
    """
    translator = get_translator()
    sl = None if source_lang.lower() == "auto" else source_lang
    results = translator.translate_texts(texts, target_lang=target_lang, source_lang=sl)
    return [result.text for result in results]
