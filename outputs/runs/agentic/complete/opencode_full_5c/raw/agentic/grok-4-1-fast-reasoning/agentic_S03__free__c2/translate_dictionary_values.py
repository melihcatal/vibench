from typing import Dict
import deepl
from translation_client import get_translator

def translate_dictionary_values(dictionary: Dict[str, str], source_lang: str = "auto", target_lang: str) -> Dict[str, str]:
    """
    Translates dictionary values while preserving keys using DeepL.
    """
    texts = list(dictionary.values())
    translator = get_translator()
    sl = None if source_lang.lower() == "auto" else source_lang
    results = translator.translate_texts(texts, target_lang=target_lang, source_lang=sl)
    translated_values = [r.text for r in results]
    return dict(zip(dictionary, translated_values))
