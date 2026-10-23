import os
from google.cloud import translate_v3 as translate

# Configure the Google Cloud Translation API client
# GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication

def translate_dashboard_note(
    project_id: str,
    text_content: str,
    target_language_code: str = "es",
    source_language_code: str = "en",
) -> str:
    """Translates metric or dashboard notes for another locale using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    # The Google Cloud Translation API (translation.googleapis.com) is used here.
    if response.translations:
        return response.translations[0].translated_text
    else:
        return f"Translation failed for text: {text_content}"
