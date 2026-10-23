import os
from security_client import get_translation_client


def translate_note(text: str, target_language: str) -> str:
    client = get_translation_client()
    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT_ID"
    )  # Assuming project ID is needed for parent path

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    translated_text = response.translations[0].translated_text
    return translated_text
