from google.cloud import translate
import os


def translate_query(query: str, target_language: str = "en") -> str:
    # Google Cloud Translation API client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "target_language_code": target_language,
        }
    )

    # Assuming only one query is translated
    if response.translations:
        return response.translations[0].translated_text
    return query
