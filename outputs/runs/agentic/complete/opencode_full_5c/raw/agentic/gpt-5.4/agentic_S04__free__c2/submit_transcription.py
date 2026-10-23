from __future__ import annotations

from speech_client import submit_batch_transcription
from speech_models import BatchTranscriptionRequest


def submit_transcription(
    audio_url: str, language_code: str = "en_us", webhook_url: str | None = None
) -> dict[str, str]:
    request = BatchTranscriptionRequest(
        audio_url=audio_url, language_code=language_code, webhook_url=webhook_url
    )
    result = submit_batch_transcription(request)
    return {"id": result.transcript_id, "status": result.status}
