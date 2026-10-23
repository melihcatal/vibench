from speech_client import get_json
from speech_models import normalize_transcript


def poll_transcription(transcript_id: str):
    payload = get_json(f"/transcript/{transcript_id}")
    if payload.get("status") == "completed":
        return normalize_transcript(payload)
    return payload
