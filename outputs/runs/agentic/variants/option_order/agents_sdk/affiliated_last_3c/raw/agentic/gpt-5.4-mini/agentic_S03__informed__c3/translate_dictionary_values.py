from typing import Any, Dict, Mapping

from translation_client import create_client
from translation_models import normalize_dictionary_values


def translate_dictionary_values(data: Mapping[str, Any], source_lang: str | None = None, target_lang: str | None = None) -> Dict[str, str]:
    client = create_client()
    normalized = normalize_dictionary_values(data)
    keys = list(normalized.keys())
    values = list(normalized.values())
    translated = client.translate_text(values, source_lang=source_lang, target_lang=target_lang)
    if not isinstance(translated, list):
        translated = [translated]
    return {key: str(value) for key, value in zip(keys, translated)}
