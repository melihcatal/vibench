from __future__ import annotations

from typing import Optional

from speech_client import SpeechClientConfig, build_assemblyai_client
from speech_models import TranscriptionJob


def timestamped_transcript(job_id: str, *, include_words: bool = True) -> TranscriptionJob:
    config = SpeechClientConfig.from_env()
    client = build_assemblyai_client(config)
    transcript = client.transcripts.get(job_id)
    result = TranscriptionJob.from_assemblyai(transcript)
    if not include_words:
        result.words = []
    return result
