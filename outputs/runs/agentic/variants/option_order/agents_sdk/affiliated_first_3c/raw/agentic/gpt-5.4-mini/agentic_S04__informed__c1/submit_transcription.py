from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from speech_client import SpeechClientFactory
from speech_models import SpeechSubmission


def submit_transcription(audio_path: str, speaker_labels: bool = False, punctuate: bool = True) -> Dict[str, Any]:
    client = SpeechClientFactory.create()
    submission = SpeechSubmission(audio_url=Path(audio_path).resolve().as_uri(), speaker_labels=speaker_labels, punctuate=punctuate)
    transcript = client.transcribe(submission.audio_url)
    return {
        "id": transcript.id,
        "status": transcript.status,
        "request": submission.to_payload(),
    }
