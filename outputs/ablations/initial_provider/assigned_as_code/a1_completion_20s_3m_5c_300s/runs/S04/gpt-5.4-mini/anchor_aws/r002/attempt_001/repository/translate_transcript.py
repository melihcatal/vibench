from google.cloud import translate_v2 as translate

from speech_models import normalize_segments


def translate_transcript(payload, config=None):
    client = translate.Client()
    target_language = payload["target_language"]
    translated = []
    for segment in normalize_segments(payload.get("segments", [])):
        translated_text, _ = client.translate(segment["text"], target_language=target_language)
        translated.append({**segment, "translated_text": translated_text})
    return {"segments": translated}
