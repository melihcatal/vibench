from google.cloud import translate_v3 as translate

from speech_models import normalize_transcript


def translate_transcript(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()
    parent = f"projects/{config.get('project_id', payload.get('project_id', ''))}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [normalize_transcript(payload)],
            "mime_type": "text/plain",
            "target_language_code": payload["target_language_code"],
        }
    )
    return {"translated_text": response.translations[0].translated_text if response.translations else ""}
