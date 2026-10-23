from speech_client import get
from speech_models import normalize_transcript_text


def poll_transcription(job_id: str) -> str:
    payload = get(f"/audio/transcriptions/{job_id}")
    return normalize_transcript_text(payload)
