from __future__ import annotations

from typing import Any, Dict, Optional

from translation_client import translate_texts
from translation_models import normalize_dictionary_values


def translate_dictionary_values(
    values: Dict[str, Any],
    target_language: str,
    source_language: Optional[str] = None,
    mime_type: str = "text/plain",
) -> Dict[str, str]:
    normalized = normalize_dictionary_values(values)
    keys = list(normalized.keys())
    payload = translate_texts(
        texts=[normalized[key] for key in keys],
        source_language=source_language,
        target_language=target_language,
        mime_type=mime_type,
    )
    return {
        key: payload["translations"][index]["translatedText"]
        for index, key in enumerate(keys)
    }
