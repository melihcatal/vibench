from typing import Dict, Any, Set
from translation_client import get_translator


def translate_dictionary_values(
    d: Dict[str, Any],
    source_lang: str = "EN",
    target_lang: str = "DE",
    keys_to_skip: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    if keys_to_skip is None:
        keys_to_skip = set()
    translator = get_translator()
    new_d = d.copy()
    for key, value in d.items():
        if key not in keys_to_skip and isinstance(value, str):
            result = translator.translate_text(
                value, source_lang=source_lang, target_lang=target_lang
            )
            new_d[key] = result.text
    return new_d
