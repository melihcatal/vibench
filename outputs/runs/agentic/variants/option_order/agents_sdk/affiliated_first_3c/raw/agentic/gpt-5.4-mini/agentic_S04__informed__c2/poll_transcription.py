from __future__ import annotations

import time

import assemblyai as aai

from speech_client import load_speech_config
from speech_models import SpeechResult, normalize_transcript


def poll_transcription(transcript_id: str, timeout_seconds: int = 900, interval_seconds: int = 5) -> SpeechResult:
    cfg = load_speech_config()
    aai.settings.api_key = cfg.api_key
    transcript = aai.Transcript.get(transcript_id)

    deadline = time.time() + timeout_seconds
    while transcript.status not in {aai.TranscriptStatus.completed, aai.TranscriptStatus.error}:
        if time.time() >= deadline:
            break
        time.sleep(interval_seconds)
        transcript = aai.Transcript.get(transcript_id)

    return normalize_transcript(transcript)
