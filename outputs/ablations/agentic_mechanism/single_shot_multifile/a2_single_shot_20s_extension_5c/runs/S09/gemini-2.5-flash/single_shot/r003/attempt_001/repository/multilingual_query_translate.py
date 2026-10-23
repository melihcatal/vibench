import os
from google.cloud import translate_v3 as translate

def translate_query(query: str, target_language_code: str = "en") -> str:
    """Translates a query into a target language using Google Cloud Translation API.
    Assumes the source language is auto-detected. Returns the translated text."""
    
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query],
            "target_language_code": target_language_code,
        }
    )

    # The response contains one translation for each input text
    for translation in response.translations:
        return translation.translated_text
    
    return query # Should not happen if API call succeeds