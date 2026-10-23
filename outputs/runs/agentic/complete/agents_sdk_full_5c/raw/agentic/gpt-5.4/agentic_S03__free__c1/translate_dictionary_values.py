from __future__ import annotations

from typing import Dict, Optional

from translation_client import get_google_parent, get_translate_client


TRANSLATION_MODEL = "general/nmt"


def translate_dictionary_values(
    values: Dict[str, str],
    target_language: str,
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
) -> Dict[str, str]:
    client = get_translate_client()
    parent = get_google_parent(project_id=project_id, location=location)
    keys = list(values.keys())
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [values[key] for key in keys],
            "target_language_code": target_language,
            "mime_type": "text/plain",
            **({"source_language_code": source_language} if source_language else {}),
            "model": f"projects/{parent.split('/')[1]}/locations/{parent.split('/')[-1]}/models/{TRANSLATION_MODEL}",
        }
    )
    return {key: item.translated_text for key, item in zip(keys, response.translations)}
