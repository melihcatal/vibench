from google.cloud import translate_v3 as translate
from speech_models import normalize_transcript


def live_caption_translate(payload, config=None):
    config = config or {}
    client = translate.TranslationServiceClient()
    parent = f"projects/{config.get('project_id')}/locations/{config.get('location', 'global')}"
    response = client.translate_text(
        parent=parent,
        contents=[payload["text"]],
        mime_type="text/plain",
        target_language_code=payload["target_language_code"],
    )
    translated = response.translations[0].translated_text if response.translations else ""
    return normalize_transcript(translated, payload.get("is_final", False), payload.get("target_language_code"))
