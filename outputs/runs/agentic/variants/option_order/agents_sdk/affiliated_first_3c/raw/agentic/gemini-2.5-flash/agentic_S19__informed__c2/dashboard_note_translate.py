import os
from google.cloud import translate_v3 as translate

def translate_dashboard_note(text: str, target_language_code: str, project_id: str = None) -> str:
    """
    Translates metric or dashboard notes for another locale using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()

    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts[0] if translated_texts else ""
