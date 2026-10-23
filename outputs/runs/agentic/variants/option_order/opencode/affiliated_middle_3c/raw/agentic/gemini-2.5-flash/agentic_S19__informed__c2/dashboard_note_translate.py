import os
from google.cloud import translate_v3 as translate


def translate_dashboard_note(
    text: str, target_language_code: str, project_id: str = None
):
    """
    Translates metric or dashboard notes for another locale using Google Cloud Translation.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translations = [
        translation.translated_text for translation in response.translations
    ]
    return translations[0] if translations else ""
