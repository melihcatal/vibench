import os
from typing import List
from google.cloud import translate_v3 as translate
from observability_client import get_translation_client
from observability_models import TranslatedMessage

def translate_log_messages(messages: List[str], target_language_code: str, project_id: str = None) -> List[TranslatedMessage]:
    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set, or project_id not provided.")

    client = get_translation_client()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": messages,
            "target_language_code": target_language_code,
        }
    )

    translated_results = []
    for i, translation in enumerate(response.translations):
        translated_results.append(TranslatedMessage(
            original_text=messages[i],
            translated_text=translation.translated_text,
            target_language_code=target_language_code
        ))
    return translated_results

