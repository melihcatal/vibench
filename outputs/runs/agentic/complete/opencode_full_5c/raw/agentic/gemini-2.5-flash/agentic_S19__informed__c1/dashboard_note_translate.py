from google.cloud import translate
import os


def translate_dashboard_note(text: str, target_language: str, project_id: str) -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
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

    translations = [
        translation.translated_text for translation in response.translations
    ]
    return translations[0] if translations else ""
