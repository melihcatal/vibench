from typing import Dict, Any
from translation_client import translator
from translation_models import normalize_text, parse_translation

def translate_dictionary_values(dictionary: Dict[str, Any], source_lang: str = "auto", target_lang: str) -> Dict[str, Any]:
    translated = {}
    for key, value in dictionary.items():
        if isinstance(value, str):
            normalized = normalize_text(value)
            result = translator.translate_text(normalized, source_lang=source_lang, target_lang=target_lang)
            parsed = parse_translation(result)
            translated[key] = parsed["translated_text"]
        else:
            translated[key] = value
    return translated
