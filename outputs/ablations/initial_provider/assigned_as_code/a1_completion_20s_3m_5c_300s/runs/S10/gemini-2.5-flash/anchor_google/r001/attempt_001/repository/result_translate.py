import os
from google.cloud import translate_v3 as translate

def translate_text(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()

    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT not found in config or environment variables.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload["text"]],
            "target_language_code": payload["target_language"],
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return {"translated_text": translated_texts[0] if translated_texts else ""}
