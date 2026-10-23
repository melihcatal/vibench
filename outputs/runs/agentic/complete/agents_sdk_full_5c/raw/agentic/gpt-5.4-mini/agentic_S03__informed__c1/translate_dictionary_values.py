from __future__ import annotations

from typing import Any, Dict

from translation_client import get_amazon_translate_client, load_translation_config
from translation_models import normalize_language_code


def translate_dictionary_values(data: Dict[str, Any], source_language: str | None = None, target_language: str | None = None) -> Dict[str, Any]:
    config = load_translation_config()
    source = normalize_language_code(source_language or config.source_language or "auto")
    target = normalize_language_code(target_language or config.target_language or "en")
    client = get_amazon_translate_client(config)
    translated: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, str):
            result = client.translate_text(Text=value, SourceLanguageCode=source, TargetLanguageCode=target)
            translated[key] = result["TranslatedText"]
        else:
            translated[key] = value
    return translated
