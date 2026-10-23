import requests

from speech_client import build_audio_url, get_base_url, get_headers
from speech_models import TranscriptionRequest, TranscriptionResponse


def submit_transcription(
    audio_file_url: str, webhook_url: str = None
) -> TranscriptionResponse:
    payload = TranscriptionRequest(
        audio_url=build_audio_url(audio_file_url), webhook_url=webhook_url
    )
    response = requests.post(
        f"{get_base_url()}/transcript",
        headers=get_headers(),
        json={"audio_url": payload.audio_url, "webhook_url": payload.webhook_url},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return TranscriptionResponse(
        provider="assemblyai", job_id=data["id"], status=data["status"]
    )
