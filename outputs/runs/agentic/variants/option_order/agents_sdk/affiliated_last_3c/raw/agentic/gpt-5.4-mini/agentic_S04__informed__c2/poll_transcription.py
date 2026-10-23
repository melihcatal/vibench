from __future__ import annotations

import time
from typing import Optional

import assemblyai as aai

from speech_client import create_client
from speech_models import normalize_assemblyai_result


def poll_transcription(transcript_id: str, timeout_s: int = 600, interval_s: int = 5):
    create_client()
    transcript = aai.Transcript.get(transcript_id)
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        transcript.refresh()
        if transcript.status in {aai.TranscriptStatus.completed, aai.TranscriptStatus.error}:
            break
        time.sleep(interval_s)
    return normalize_assemblyai_result(transcript)
