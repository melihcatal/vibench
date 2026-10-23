from __future__ import annotations

from typing import Any, Dict, Optional

from translation_client import build_translation_client, normalize_translation_languages
from translation_models import normalize_mapping_values


def translate_dictionary_values(
    data: Dict[str, Any],
    target_language: str,
    source_language: Optional[str] = None,
    mime_type: str = "text/plain",
) -> Dict[str, str]:
    client, parent, model_path = build_translation_client()
    source_language, target_language = normalize_translation_languages(source_language, target_language)
    normalized = normalize_mapping_values(data)
    keys = list(normalized.keys())
    values = [normalized[key] for key in keys]
    if not values:
        return {}

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": values,
            "mime_type": mime_type,
            "target_language_code": target_language,
            "source_language_code": source_language,
            "model": model_path,
        }
    )
    return {key: item.translated_text for key, item in zip(keys, response.translations)}
