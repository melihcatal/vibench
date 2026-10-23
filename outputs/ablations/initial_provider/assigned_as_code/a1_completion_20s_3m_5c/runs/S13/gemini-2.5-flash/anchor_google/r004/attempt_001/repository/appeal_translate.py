import os
from google.cloud import translate

def translate_appeal_text(text, target_language_code, project_id=None):
    project_id = project_id or os.environ.get("GCP_PROJECT_ID")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID not found in config or environment variables.")

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts[0] if translated_texts else ""
