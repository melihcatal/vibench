import requests

from speech_client import build_audio_url, get_base_url, get_headers
from speech_models import TranscriptionResponse, normalize_segments


def diarized_transcript(audio_file_url: str) -> TranscriptionResponse:
    response = requests.post(
        f"{get_base_url()}/transcript",
        headers=get_headers(),
        json={"audio_url": build_audio_url(audio_file_url), "speaker_labels": True},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return TranscriptionResponse(
        provider="assemblyai",
        job_id=data["id"],
        status=data["status"],
        transcript=data.get("text", ""),
        segments=normalize_segments(data.get("utterances") or data.get("segments")),
    )
