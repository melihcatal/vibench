from translation_client import get_translator
from typing import Dict, Any

def translate_dictionary_values(d: Dict[str, Any], source_lang: str = "EN", target_lang: str = "ES") -> Dict[str, str]:
    """
    Translates dictionary values while preserving keys using DeepL.
    """
    translator = get_translator()
    values = [str(v) for v in d.values()]
    results = translator.translate_text(values, source_lang=source_lang, target_lang=target_lang)
    return dict(zip(d, [r.text for r in results]))