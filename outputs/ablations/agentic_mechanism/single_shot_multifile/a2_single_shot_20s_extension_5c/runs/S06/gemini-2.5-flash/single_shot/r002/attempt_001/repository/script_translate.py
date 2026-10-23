import os
from google.cloud import translate_v3beta1 as translate

def translate_script(
    text: str,
    target_language_code: str,
    source_language_code: str = None,
    project_id: str = None
) -> str:
    """
    Translates text using Google Cloud Translation API.
    """
    if project_id is None:
        project_id = os.environ.get("GCP_PROJECT_ID")
        if not project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        model="projects/project-number-or-id/locations/global/models/general/nmt" # Example model name
    )

    if response.translations:
        return response.translations[0].translated_text
    return text
