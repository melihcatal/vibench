from google.cloud import translate_v3
from translation_client import get_translation_client

def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    """Translates a single text string between languages using Google Cloud Translation."""
    client = get_translation_client()
    project_id = "your-gcp-project-id"  # Replace with your GCP project ID
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
            "source_language_code": source_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
