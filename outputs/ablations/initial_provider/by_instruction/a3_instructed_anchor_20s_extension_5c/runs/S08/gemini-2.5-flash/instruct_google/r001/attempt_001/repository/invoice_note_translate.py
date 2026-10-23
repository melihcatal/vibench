import os
from google.cloud import translate_v3beta1 as translate

def translate_invoice_notes(text: str, target_language: str = "en") -> dict:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()

    location = "global" # Or a specific region if needed
    parent = f"projects/{project_id}/locations/{location}"

    try:
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
            "original_text": text,
            "translated_text": translations[0] if translations else "",
            "target_language": target_language,
            "provider": "google_cloud_translation"
        }

    except Exception as e:
        return {
            "original_text": text,
            "translated_text": "",
            "target_language": target_language,
            "error": str(e),
            "provider": "google_cloud_translation"
        }
