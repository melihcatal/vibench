from __future__ import annotations

from typing import List

from speech_client import AssemblyAISpeechClient
from speech_models import (
    TranscriptionSubmitRequest,
    TranscriptSegment,
    normalize_transcript_response,
)


def diarized_transcript(
    audio_url: str,
    speakers_expected: int | None = None,
    language_code: str | None = None,
) -> List[TranscriptSegment]:
    client = AssemblyAISpeechClient()
    response = client.submit_transcript(
        TranscriptionSubmitRequest(
            audio_url=audio_url,
            language_code=language_code,
            speaker_labels=True,
            speakers_expected=speakers_expected,
        )
    )
    transcript = normalize_transcript_response(response)
    return transcript.utterances
