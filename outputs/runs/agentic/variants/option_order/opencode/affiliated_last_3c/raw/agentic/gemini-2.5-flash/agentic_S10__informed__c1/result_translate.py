import os
from google.cloud import translate_v3 as translate


def translate_text(
    text: str,
    target_language_code: str,
    project_id: str = os.environ.get("GOOGLE_CLOUD_PROJECT"),
) -> str:
    """
    Translates text into the target language using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up for authentication.
    """
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    return response.translations[0].translated_text
