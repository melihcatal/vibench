from translation_client import get_translator
from translation_models import normalize_texts, extract_translated_texts
from typing import Dict, Any
from deepl import Translator

def translate_dictionary_values(d: Dict[str, str], source_lang: str = "auto", target_lang: str = "EN") -> Dict[str, str]:
    keys = list(d.keys())
    values = list(d.values())
    translator = get_translator()
    normalized = normalize_texts(values)
    results = translator.translate_texts(normalized, source_lang=source_lang, target_lang=target_lang)
    translated_values = extract_translated_texts(results)
    return dict(zip(keys, translated_values))