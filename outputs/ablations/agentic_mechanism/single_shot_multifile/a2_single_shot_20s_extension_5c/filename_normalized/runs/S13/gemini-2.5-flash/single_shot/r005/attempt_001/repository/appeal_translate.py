import os
from google.cloud import translate_v3
from safety_client import load_google_translate_client
from safety_models import AppealRequest

def translate_appeal_text(appeal_request: AppealRequest, target_language_code: str = "en") -> str:
    client = load_google_translate_client()

    project_id = os.environ.get("GCP_PROJECT_ID") # Required for Cloud Translation V3
    if not project_id: raise ValueError("GCP_PROJECT_ID environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [appeal_request.user_appeal_reason],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text = translation.translated_text
        break # Assuming only one content in the list
    
    return translated_text
