import os
from typing import Dict, Optional, List
from google.cloud import translate_v3 as translate
from translation_client import get_translation_client, get_project_id, get_location
from translation_models import DictionaryTranslationResult

def translate_dict_values(
    data_dict: Dict[str, str],
    target_language: str,
    source_language: Optional[str] = None,
    mime_type: str = "text/plain",
) -> DictionaryTranslationResult:
    client = get_translation_client()
    project_id = get_project_id()
    location = get_location()

    parent = f"projects/{project_id}/locations/{location}"

    original_keys = list(data_dict.keys())
    original_values = [data_dict[key] for key in original_keys]

    if not original_values:
        return DictionaryTranslationResult(translated_dictionary={})

    response = client.translate_text(
        parent=parent,
        contents=original_values,
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type=mime_type,
    )

    translated_values = [t.translated_text for t in response.translations]

    translated_dict = {}
    for i, key in enumerate(original_keys):
        translated_dict[key] = translated_values[i]

    return DictionaryTranslationResult(translated_dictionary=translated_dict)
