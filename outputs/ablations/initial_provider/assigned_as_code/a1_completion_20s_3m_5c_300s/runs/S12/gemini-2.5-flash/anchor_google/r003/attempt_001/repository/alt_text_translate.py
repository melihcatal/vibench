from google.cloud import translate_v3 as translate
import os


def alt_text_translate(payload, config=None):
    config = config or {}
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    text_to_translate = payload.get("description", "")
    target_language = config.get("target_language", "es")

    if not text_to_translate:
        return {"translated_text": ""}

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_to_translate],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text if response.translations else ""
    return {"translated_text": translated_text}
