import os
from typing import Dict, Any, Optional
from translation_client import get_translation_client, get_location_path
from translation_models import TranslationRequest, TranslationResponse

def translate_dictionary_values(
    data: Dict[str, str],
    target_language_code: str,
    source_language_code: Optional[str] = None
) -> Dict[str, str]:
    if not data:
        return {}

    keys = list(data.keys())
    values_to_translate = list(data.values())

    if not values_to_translate:
        return data

    client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    parent = get_location_path(project_id, location)
    
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": values_to_translate,
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
            "mime_type": "text/plain",
        }
    )
    
    translated_values = [t.translated_text for t in response.translations]
    
    translated_data = {}
    for i, key in enumerate(keys):
        translated_data[key] = translated_values[i]
            
    return translated_data