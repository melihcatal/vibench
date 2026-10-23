from google.cloud import translate_v3 as translate
import os

def alt_text_translate(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # Or pass as config
    location = config.get("location", "global")

    parent = f"projects/{project_id}/locations/{location}"

    text_to_translate = payload["text"]
    target_language_code = payload.get("target_language", "es") # Default to Spanish

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_to_translate],
            "mime_type": "text/plain",
            "source_language_code": "en", # Assuming source is English
            "target_language_code": target_language_code,
        }
    )

    translations = []
    for translation in response.translations:
        translations.append(translation.translated_text)

    return {"translated_text": translations[0] if translations else ""}
