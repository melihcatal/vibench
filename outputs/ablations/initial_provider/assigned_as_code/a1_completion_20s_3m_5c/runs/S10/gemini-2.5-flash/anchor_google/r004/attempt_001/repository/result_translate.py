import os
from google.cloud import translate_v3 as translate
from model_client import get_translate_client

def result_translate(payload, config=None):
    config = config or {}
    text = payload["text"]
    target_language_code = payload["target_language_code"]
    source_language_code = payload.get("source_language_code", "en")
    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided in config or GOOGLE_CLOUD_PROJECT environment variable.")

    client = get_translate_client(project_id=project_id)
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    
    return {"translated_text": translated_text}
