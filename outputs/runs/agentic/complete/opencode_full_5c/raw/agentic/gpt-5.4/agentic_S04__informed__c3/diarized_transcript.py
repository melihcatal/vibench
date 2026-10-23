from __future__ import annotations

from speech_client import build_transcription_config, get_assemblyai_client
from speech_models import (
    TranscriptResult,
    TranscriptionRequest,
    normalize_assemblyai_transcript,
)


def diarized_transcript(
    audio_url: str, speakers_expected: int | None = None
) -> TranscriptResult:
    client = get_assemblyai_client()
    request = TranscriptionRequest(
        audio_url=audio_url,
        speaker_labels=True,
        speakers_expected=speakers_expected,
    )
    transcript = client.transcribe(
        request.audio_url, config=build_transcription_config(request)
    )
    return normalize_assemblyai_transcript(transcript)
