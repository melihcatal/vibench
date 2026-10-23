from __future__ import annotations

from speech_client import submit_batch_transcription
from speech_models import BatchTranscriptionRequest


def diarized_transcript(
    audio_url: str, speakers_expected: int | None = None, language_code: str = "en_us"
) -> dict[str, object]:
    request = BatchTranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        enable_speaker_labels=True,
        speakers_expected=speakers_expected,
    )
    result = submit_batch_transcription(request)
    return {
        "id": result.transcript_id,
        "status": result.status,
        "speaker_labels": True,
    }
