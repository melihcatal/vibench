from __future__ import annotations

from typing import Any

import assemblyai as aai

from speech_client import SpeechClientConfig, build_assemblyai_client
from speech_models import TranscriptionJob


def poll_transcription(job_id: str) -> TranscriptionJob:
    config = SpeechClientConfig.from_env()
    client = build_assemblyai_client(config)
    transcript = client.transcripts.get(job_id)
    if getattr(transcript, "status", None) in {aai.TranscriptStatus.queued, aai.TranscriptStatus.processing}:
        transcript = client.transcripts.get(job_id)
    return TranscriptionJob.from_assemblyai(transcript)
