import os
from typing import Dict
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_dict_values(
    data: Dict[str, str], target_language: str, source_language: str
) -> Dict[str, str]:
    """
    Translates dictionary values while preserving keys using Google Cloud Translation.
    """
    client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    if not data:
        return {}

    keys = list(data.keys())
    contents = [data[key] for key in keys]

    response = client.translate_text(
        parent=parent,
        contents=contents,
        target_language_code=target_language,
        source_language_code=source_language,
    )

    translated_dict = {}
    for i, translation in enumerate(response.translations):
        translated_dict[keys[i]] = translation.translated_text

    return translated_dict
