from __future__ import annotations

from speech_client import build_transcription_config, get_assemblyai_client
from speech_models import TranscriptionJob, TranscriptionRequest


def submit_transcription(
    audio_url: str, language_code: str | None = None
) -> TranscriptionJob:
    client = get_assemblyai_client()
    request = TranscriptionRequest(audio_url=audio_url, language_code=language_code)
    transcript = client.submit(
        request.audio_url, config=build_transcription_config(request)
    )
    return TranscriptionJob(
        transcript_id=transcript.id,
        status=transcript.status,
        audio_url=audio_url,
    )
