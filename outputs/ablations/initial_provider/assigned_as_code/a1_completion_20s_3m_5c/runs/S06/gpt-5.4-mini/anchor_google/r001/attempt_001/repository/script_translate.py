from google.cloud import translate_v3 as translate

from speech_models import normalize_payload


def script_translate(payload, config=None):
    payload = normalize_payload(payload)
    config = dict(config or {})
    client = translate.TranslationServiceClient()
    parent = client.common_location_path(config.get("project_id", ""), config.get("location", "global"))
    response = client.translate_text(contents=[payload.get("text", "")], target_language_code=config.get("target_language_code", "en"), parent=parent, mime_type="text/plain")
    return {"translated_text": response.translations[0].translated_text if response.translations else "", "provider": "google-cloud-translate"}
