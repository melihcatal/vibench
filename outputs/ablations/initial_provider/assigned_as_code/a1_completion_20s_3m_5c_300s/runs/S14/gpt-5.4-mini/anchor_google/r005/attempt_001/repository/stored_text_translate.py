from google.cloud import translate_v3

from storage_client import storage_client


def stored_text_translate(payload, config=None):
    _, config = storage_client(config)
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path(config["project_id"], config.get("location", "global"))
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload["text"]],
            "mime_type": "text/plain",
            "target_language_code": payload["target_language_code"],
        }
    )
    return {"translated_text": response.translations[0].translated_text}
