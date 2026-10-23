from __future__ import annotations

import os
from pathlib import Path

import assemblyai as aai

from speech_models import TranscriptResult


ASSEMBLYAI_MODEL = "best"


def transcribe_qa_sample(audio_path: str) -> TranscriptResult:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise EnvironmentError("ASSEMBLYAI_API_KEY is required for AssemblyAI Transcripts API")
    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(speech_model=ASSEMBLYAI_MODEL)
    transcript = aai.Transcriber(config=config).transcribe(str(Path(audio_path)))
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(transcript.error)
    return TranscriptResult(
        provider="assemblyai",
        transcript=transcript.text or "",
        confidence=getattr(transcript, "confidence", None),
        raw={"id": transcript.id, "status": str(transcript.status)},
    )
