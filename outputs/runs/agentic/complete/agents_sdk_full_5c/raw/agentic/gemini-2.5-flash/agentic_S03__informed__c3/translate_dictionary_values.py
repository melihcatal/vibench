from translation_client import get_translation_client, get_project_id
from translation_models import TranslationRequest, TranslationResponse
from typing import Dict, Any

def translate_dictionary_values(
    data: Dict[str, Any],
    target_language: str,
    source_language: str = None,
    project_id: str = None,
) -> Dict[str, Any]:
    """
    Translates string values within a dictionary using Google Cloud Translation,
    preserving keys and other non-string values.
    """
    client = get_translation_client()
    if project_id is None:
        project_id = get_project_id()
    parent = f"projects/{project_id}/locations/global"

    texts_to_translate = []
    keys_to_translate = []

    for key, value in data.items():
        if isinstance(value, str):
            texts_to_translate.append(value)
            keys_to_translate.append(key)

    if not texts_to_translate:
        return data

    request = {
        "parent": parent,
        "contents": texts_to_translate,
        "target_language_code": target_language,
        "mime_type": "text/plain",
    }
    if source_language:
        request["source_language_code"] = source_language

    response = client.translate_text(request=request)
    translated_texts = [translation.translated_text for translation in response.translations]

    translated_data = data.copy()
    for i, key in enumerate(keys_to_translate):
        translated_data[key] = translated_texts[i]

    return translated_data
