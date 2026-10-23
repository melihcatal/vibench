from google.cloud import translate
import os


def translate_record_field(text: str, target_language: str, project_id: str):
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    client = translate.TranslationServiceClient()
    location = "global"  # Or specific region for advanced models

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)

    return {
        "status": "success",
        "translated_text": translations[0] if translations else None,
    }
