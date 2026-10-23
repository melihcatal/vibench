from typing import Dict, Any
from google.cloud import translate_v3
from translation_client import get_translation_service_client, get_project_id, get_location
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(payload: DictionaryTranslationRequest, config: Dict[str, Any] = None) -> DictionaryTranslationResponse:
    config = config or {}
    client = get_translation_service_client()
    project_id = config.get("project_id", get_project_id())
    location = config.get("location", get_location())
    parent = f"projects/{project_id}/locations/{location}"

    original_keys = list(payload.dictionary.keys())
    original_values = list(payload.dictionary.values())

    # Translate all values in a single batch request
    response = client.translate_text(request={
        "parent": parent,
        "contents": original_values,
        "mime_type": "text/plain", # Assuming dictionary values are plain text
        "source_language_code": payload.source_language,
        "target_language_code": payload.target_language,
    })

    translated_values = [translation.translated_text for translation in response.translations]

    translated_dictionary = dict(zip(original_keys, translated_values))

    return DictionaryTranslationResponse(
        translated_dictionary=translated_dictionary,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
