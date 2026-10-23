import os
from google.cloud import translate_v3 as translate


def translate_query(
    query: str, target_language: str, project_id: str | None = None
) -> str:
    """Translates queries before multilingual embedding search using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()

    if project_id is None:
        # Attempt to get project_id from environment variable, common in Google Cloud environments.
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set."
            )

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "target_language_code": target_language,
        }
    )

    # Display the translation for the first input. (There's only one input in this case)
    for translation in response.translations:
        return translation.translated_text
    return ""
