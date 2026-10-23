import os
from google.cloud import translate_v3 as translate
from safety_client import SafetyClient

def translate_appeal_text(text: str, target_language: str = "en") -> str:
    """
    Translates appeal text for review using Google Cloud Translation API.
    Defaults to translating to English.
    """
    safety_client = SafetyClient()
    project_id = safety_client.project_id
    location = safety_client.location # Translation API typically uses 'global' or specific regions

    # The Translation API v3 uses a regional endpoint, usually 'global'
    # For this example, we'll use global, but it can be specified if needed.
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "target_language_code": target_language,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return translated_text
