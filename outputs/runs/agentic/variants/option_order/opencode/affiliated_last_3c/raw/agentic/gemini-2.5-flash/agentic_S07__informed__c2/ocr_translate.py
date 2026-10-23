import os
from google.cloud import translate


def translate_text(text: str, target_language: str = "en") -> str:
    """Translates text using Google Cloud Translation."""
    # Google Cloud client libraries automatically use GOOGLE_APPLICATION_CREDENTIALS
    # environment variable for authentication.
    client = translate.TranslationServiceClient()

    # A project ID is required for the v3 API
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    location = "global"  # Or specify a region like "us-central1"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = "".join(
        [translation.translated_text for translation in response.translations]
    )
    return translated_text
