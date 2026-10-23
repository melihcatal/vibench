from google.cloud import translate_v3
from translation_client import get_translation_client

def batch_translate(texts: list[str], target_language: str, source_language: str = "en") -> list[str]:
    """Translates a list of strings while preserving order using Google Cloud Translation."""
    client = get_translation_client()
    project_id = "your-gcp-project-id"  # Replace with your GCP project ID
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "target_language_code": target_language,
            "source_language_code": source_language,
        }
    )

    return [translation.translated_text for translation in response.translations]
