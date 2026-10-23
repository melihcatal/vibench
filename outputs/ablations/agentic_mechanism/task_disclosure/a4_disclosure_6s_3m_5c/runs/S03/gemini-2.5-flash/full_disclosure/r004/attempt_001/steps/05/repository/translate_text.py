from google.cloud import translate

def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    """Translates a single text string between languages using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    project_id = "your-gcp-project-id"  # Replace with your Google Cloud Project ID
    location = "global"  # Or specific region like "us-central1"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Set to "text/html" for HTML content
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    for translation in response.translations:
        return translation.translated_text
    return ""

