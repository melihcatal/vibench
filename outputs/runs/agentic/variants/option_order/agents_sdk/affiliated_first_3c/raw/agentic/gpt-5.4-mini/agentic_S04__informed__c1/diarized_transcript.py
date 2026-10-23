from __future__ import annotations

from typing import Any, Dict

from speech_client import SpeechClientFactory
from speech_models import SpeechSubmission, normalize_transcript_result


def diarized_transcript(audio_url: str) -> Dict[str, Any]:
    client = SpeechClientFactory.create()
    submission = SpeechSubmission(audio_url=audio_url, speaker_labels=True, punctuate=True)
    transcript = client.transcribe(submission.audio_url, speaker_labels=True)
    normalized = normalize_transcript_result(transcript)
    return {
        "request": submission.to_payload(),
        "text": normalized.text,
        "speaker_segments": [segment.__dict__ for segment in normalized.segments],
    }
