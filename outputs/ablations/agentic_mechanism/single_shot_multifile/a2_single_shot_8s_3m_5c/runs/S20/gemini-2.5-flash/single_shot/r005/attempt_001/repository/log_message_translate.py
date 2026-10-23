from observability_client import get_translation_client, get_gcp_project_id
from typing import List, Dict

def translate_log_messages(messages: List[str], target_language_code: str, source_language_code: str = "en") -> Dict[str, str]:
    client = get_translation_client()
    project_id = get_gcp_project_id()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": messages,
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    translated_texts = {}
    for i, translation in enumerate(response.translations):
        translated_texts[messages[i]] = translation.translated_text
    
    return translated_texts