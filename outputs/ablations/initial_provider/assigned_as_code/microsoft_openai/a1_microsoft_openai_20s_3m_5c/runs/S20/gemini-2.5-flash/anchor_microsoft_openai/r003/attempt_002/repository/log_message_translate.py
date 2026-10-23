from google.cloud import translate_v3 as translate
import os

def translate_log_message(text: str, target_language_code: str = "es") -> str:
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Ensure GOOGLE_CLOUD_PROJECT is set
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text

    return translated_text
