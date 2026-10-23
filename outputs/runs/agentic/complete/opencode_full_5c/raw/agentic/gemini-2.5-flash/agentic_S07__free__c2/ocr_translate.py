from document_client import get_translation_client, get_project_id, get_location
from google.cloud import translate_v3


def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    client = get_translation_client()
    project_id = get_project_id()
    location = get_location()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_text = response.translations[0].translated_text
    return translated_text
