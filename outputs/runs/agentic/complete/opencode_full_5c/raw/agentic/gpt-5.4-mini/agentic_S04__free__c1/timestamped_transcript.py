from speech_client import get
from speech_models import normalize_segments


def timestamped_transcript(job_id: str) -> list:
    payload = get(f"/audio/transcriptions/{job_id}")
    return normalize_segments(payload)
