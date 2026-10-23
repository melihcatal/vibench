from typing import Dict, Any
from translation_client import get_translator
from translation_models import normalize_input, normalize_output
from deepl import Translator

def translate_dictionary_values(d: Dict[str, Any], source_lang: str = "auto", target_lang: str) -> Dict[str, Any]:
    new_d = d.copy()
    str_items = [(k, v) for k, v in d.items() if isinstance(v, str)]
    if not str_items:
        return new_d
    keys, values = zip(*str_items)
    normalized_values = [normalize_input(v) for v in values]
    translator: Translator = get_translator()
    results = translator.translate_text(normalized_values, source_lang=source_lang, target_lang=target_lang)
    translated_values = [normalize_output(r.text) for r in results]
    for key, trans_val in zip(keys, translated_values):
        new_d[key] = trans_val
    return new_d