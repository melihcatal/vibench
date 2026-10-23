import os
from google.cloud import translate_v3 as translate


def translate_query(query: str, target_language: str) -> str:
    """
    Translates a query into a target language using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up for authentication.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[query],
        target_language_code=target_language,
        mime_type="text/plain",
    )

    if response.translations:
        return response.translations[0].translated_text
    return query  # Return original query if no translation occurs
