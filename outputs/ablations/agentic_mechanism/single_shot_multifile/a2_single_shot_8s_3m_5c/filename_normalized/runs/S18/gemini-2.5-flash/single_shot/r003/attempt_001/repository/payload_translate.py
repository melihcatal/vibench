import os
from google.cloud import translate_v3 as translate
from messaging_client import get_gcp_translate_client
from messaging_models import EventMessage

def translate_payload_text(message: EventMessage, target_language_code: str = "es") -> dict:
    client = get_gcp_translate_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}"
    
    translated_payload = message.payload.copy()
    for key, value in translated_payload.items():
        if isinstance(value, str):
            response = client.translate_text(
                parent=parent,
                contents=[value],
                target_language_code=target_language_code,
                mime_type="text/plain",
            )
            if response.translations:
                translated_payload[key] = response.translations[0].translated_text

    return translated_payload
