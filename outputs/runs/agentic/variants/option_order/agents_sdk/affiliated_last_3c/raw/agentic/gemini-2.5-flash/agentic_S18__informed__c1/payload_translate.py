import os
from typing import Dict, Any, List
from messaging_client import get_translate_client
from google.cloud.translate_v3.types import TranslateTextRequest

def translate_payload_text(payload: Dict[str, Any], target_language_code: str = "es", source_language_code: str = "en") -> Dict[str, Any]:
    """Translates customer-facing message payload text using Google Cloud Translation.
       It attempts to translate string values within the payload.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = get_translate_client()
    parent = f"projects/{project_id}/locations/global"

    translated_payload = payload.copy()
    texts_to_translate: List[str] = []
    text_paths: List[List[str]] = []

    def collect_texts(obj, current_path):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str) and value.strip():  # Only translate non-empty strings
                    texts_to_translate.append(value)
                    text_paths.append(current_path + [key])
                elif isinstance(value, (dict, list)):
                    collect_texts(value, current_path + [key])
        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                if isinstance(value, str) and value.strip():
                    texts_to_translate.append(value)
                    text_paths.append(current_path + [str(i)]) # Use string index for path
                elif isinstance(value, (dict, list)):
                    collect_texts(value, current_path + [str(i)])

    collect_texts(translated_payload, [])

    if not texts_to_translate:
        return translated_payload

    request = TranslateTextRequest(
        parent=parent,
        contents=texts_to_translate,
        mime_type="text/plain",
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    response = client.translate_text(request=request)

    for i, translation in enumerate(response.translations):
        path = text_paths[i]
        current_obj = translated_payload
        for j, key_or_index in enumerate(path):
            if j == len(path) - 1:
                if isinstance(current_obj, dict):
                    current_obj[key_or_index] = translation.translated_text
                elif isinstance(current_obj, list):
                    current_obj[int(key_or_index)] = translation.translated_text
            else:
                if isinstance(current_obj, dict):
                    current_obj = current_obj[key_or_index]
                elif isinstance(current_obj, list):
                    current_obj = current_obj[int(key_or_index)]

    return translated_payload
