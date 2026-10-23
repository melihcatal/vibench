import os
from google.cloud import translate_v3 as translate

def translate_query(query: str, target_language: str) -> str:
    """
    Translates a query to a target language using Google Cloud Translation API.

    Args:
        query: The text query to translate.
        target_language: The language to translate the query into (e.g., "en", "es", "fr").

    Returns:
        The translated query.
    """
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query],
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return query

