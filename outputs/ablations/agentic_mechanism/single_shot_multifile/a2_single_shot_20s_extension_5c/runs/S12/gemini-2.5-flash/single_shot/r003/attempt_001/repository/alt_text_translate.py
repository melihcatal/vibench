import os
from google.cloud.translate_v3 import TranslationServiceClient, TranslationConfig
from vision_client import get_google_translate_client
from vision_models import parse_google_translate_result

def translate_alt_text(text: str, target_language_code: str = "es", source_language_code: str = "en"):
    client = get_google_translate_client()
    gcp_project_id = os.environ.get('GCP_PROJECT_ID')
    if not gcp_project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set for Google Translate.")
    
    parent = f"projects/{gcp_project_id}/locations/global"
    
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "model": f"projects/{gcp_project_id}/locations/global/models/general/nmt"
        }
    )
    return parse_google_translate_result(response)
