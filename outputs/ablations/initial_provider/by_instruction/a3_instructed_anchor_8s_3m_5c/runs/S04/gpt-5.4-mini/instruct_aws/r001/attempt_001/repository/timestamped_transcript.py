from speech_models import normalize_segments


def extract_timestamped_transcript(transcription_result):
    payload = transcription_result.get("Transcript") if isinstance(transcription_result, dict) else None
    items = []
    if payload and isinstance(payload, dict):
        results = payload.get("Results") or {}
        items = results.get("Items") or []
    return normalize_segments(items)
