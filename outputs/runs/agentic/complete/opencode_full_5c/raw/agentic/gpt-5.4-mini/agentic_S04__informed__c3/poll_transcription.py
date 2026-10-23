import requests

from speech_client import get_base_url, get_headers
from speech_models import TranscriptionResponse, normalize_segments


def poll_transcription(job_id: str) -> TranscriptionResponse:
    response = requests.get(
        f"{get_base_url()}/transcript/{job_id}", headers=get_headers(), timeout=60
    )
    response.raise_for_status()
    data = response.json()
    return TranscriptionResponse(
        provider="assemblyai",
        job_id=job_id,
        status=data.get("status", ""),
        transcript=data.get("text", ""),
        segments=normalize_segments(data.get("segments")),
    )
