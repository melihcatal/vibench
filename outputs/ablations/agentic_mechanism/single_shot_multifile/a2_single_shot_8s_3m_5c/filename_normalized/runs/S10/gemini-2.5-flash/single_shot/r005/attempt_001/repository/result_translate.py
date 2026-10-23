import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language: str = "en", project_id: Optional[str] = None) -> str:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return text