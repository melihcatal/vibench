from google.cloud import translate_v3 as translate
from document_client import get_translation_client
import os


def translate_text(text: str, target_language_code: str = "en") -> str:
    client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get(
        "GOOGLE_CLOUD_LOCATION", "global"
    )  # Translation API often uses global or specific regions

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
