from google.cloud import translate_v3 as translate

from speech_models import normalize_text


def live_caption_translate(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()
    parent = config.get("parent") or f"projects/{config['project_id']}/locations/{config.get('location', 'global')}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [normalize_text(payload["text"])],
            "target_language_code": config["target_language_code"],
        }
    )
    return {"text": response.translations[0].translated_text if response.translations else ""}
