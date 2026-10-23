from translation_client import get_translation_client, get_parent_path
from translation_models import TranslationRequest
from typing import Dict, Any

def translate_dictionary_values(payload: Dict[str, str], source_language: str, target_language: str, config: dict = None) -> Dict[str, str]:
    config = config or {}
    client = get_translation_client()
    parent = get_parent_path(config['project_id'], config.get('location', 'global'))

    original_keys = list(payload.keys())
    original_values = [payload[key] for key in original_keys]

    if not original_values:
        return {}

    response = client.translate_text(request={
        "parent": parent,
        "contents": original_values,
        "mime_type": "text/plain",
        "source_language_code": source_language,
        "target_language_code": target_language,
    })

    translated_values = [translation.translated_text for translation in response.translations]

    translated_dict = {}
    for i, key in enumerate(original_keys):
        translated_dict[key] = translated_values[i]

    return translated_dict
