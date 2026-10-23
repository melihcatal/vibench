import os
from google.cloud import translate_v3 as translate


def record_translate(text_content: str, target_language: str = "es"):
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        return {
            "status": "error",
            "message": "GOOGLE_CLOUD_PROJECT environment variable not set.",
        }

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)

    if translations:
        return {"status": "success", "translated_text": translations[0]}
    else:
        return {"status": "error", "message": "No translation found."}
