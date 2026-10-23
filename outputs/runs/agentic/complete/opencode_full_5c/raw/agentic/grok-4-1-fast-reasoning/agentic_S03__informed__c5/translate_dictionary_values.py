from translation_client import get_translator
from translation_models import normalize_input
from typing import Dict, Any, List, Optional


def translate_dictionary_values(
    d: Dict[str, Any],
    source_lang: Optional[str] = None,
    target_lang: str = "EN-US",
    keys_to_skip: Optional[List[str]] = None,
) -> Dict[str, Any]:
    if keys_to_skip is None:
        keys_to_skip = []
    new_d = d.copy()
    translator = get_translator()
    for k, v in d.items():
        if k not in keys_to_skip and isinstance(v, str) and v.strip():
            v_normalized = normalize_input(v)
            result = translator.translate_text(
                v_normalized, source_lang=source_lang, target_lang=target_lang
            )
            new_d[k] = result.text
    return new_d
