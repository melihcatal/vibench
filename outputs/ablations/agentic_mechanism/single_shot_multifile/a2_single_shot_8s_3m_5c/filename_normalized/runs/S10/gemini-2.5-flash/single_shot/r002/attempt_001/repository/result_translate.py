import os
from google.cloud import translate_v3

def translate_text(text: str, target_language: str) -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    
    client = translate_v3.TranslationServiceClient()
    
    parent = f"projects/{project_id}/locations/global"
    
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    
    if response.translations:
        return response.translations[0].translated_text
    return text
