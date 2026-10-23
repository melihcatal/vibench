from translation_client import get_translation_client, get_project_id
from translation_models import DictionaryTranslationRequest
from google.cloud import translate_v3beta1 as translate  # Provider-specific import
from typing import Dict


def translate_dictionary_values(
    request: DictionaryTranslationRequest,
) -> Dict[str, str]:
    client = get_translation_client()
    project_id = get_project_id()
    if not project_id:
        raise ValueError(
            "Google Cloud Project ID not found. Ensure GOOGLE_CLOUD_PROJECT environment variable is set or authenticated with gcloud."
        )

    parent = f"projects/{project_id}/locations/global"

    translated_dict = {}
    for key, value in request.data.items():
        response = client.translate_text(
            parent=parent,
            contents=[value],
            target_language_code=request.target_language_code,
            source_language_code=request.source_language_code,
            mime_type="text/plain",
        )
        translated_dict[key] = response.translations[0].translated_text

    return translated_dict
