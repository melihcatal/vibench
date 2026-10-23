import os
from typing import List
from google.cloud import translate_v3 as translate  # Google Cloud Translation API


def translate_query(
    query: str, target_language_code: str, project_id: str = None
) -> str:
    """
    Translates a query into a target language using Google Cloud Translation API.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT environment variable not set and project_id not provided."
            )

    client = translate.TranslationServiceClient()
    location = "global"  # Translation API is global
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[query],
        target_language_code=target_language_code,
        source_language_code="en",  # Assuming English source for queries
        model="projects/project-number/locations/location-id/models/model-id",  # Illustrative, real models are often auto-selected
    )

    if response.translations:
        return response.translations[0].translated_text
    return query  # Return original if no translation
