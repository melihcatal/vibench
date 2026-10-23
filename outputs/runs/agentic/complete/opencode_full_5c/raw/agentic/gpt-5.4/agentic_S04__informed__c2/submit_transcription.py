from __future__ import annotations

from speech_client import AssemblyAISpeechClient
from speech_models import TranscriptionSubmitRequest, TranscriptStatus


def submit_transcription(
    audio_url: str,
    language_code: str | None = None,
    speaker_labels: bool = False,
    speakers_expected: int | None = None,
) -> TranscriptStatus:
    client = AssemblyAISpeechClient()
    payload = TranscriptionSubmitRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=speaker_labels,
        speakers_expected=speakers_expected,
    )
    response = client.submit_transcript(payload)
    return TranscriptStatus(
        transcript_id=response["id"],
        status=response.get("status", "queued"),
        error=response.get("error"),
    )
