from google.cloud import translate_v3

from document_client import get_config
from document_models import normalize_text


def ocr_translate(payload, config=None):
    config = get_config(config)
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{config['project_id']}/locations/{config['location']}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [normalize_text(payload.get("text", ""))],
            "mime_type": "text/plain",
            "target_language_code": config["translation_target_language"],
        }
    )
    translations = [item.translated_text for item in response.translations]
    return {"translations": translations}
