from google.cloud import translate
import os

def translate_caption(text: str, target_language_code: str = "es") -> str:
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set.")
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
