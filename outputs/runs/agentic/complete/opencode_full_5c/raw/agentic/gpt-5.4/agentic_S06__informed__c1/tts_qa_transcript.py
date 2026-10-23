from __future__ import annotations

import os

import assemblyai as aai

from speech_models import TranscriptResult


def transcribe_qa_sample(audio_path: str) -> TranscriptResult:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise EnvironmentError("ASSEMBLYAI_API_KEY is required")
    aai.settings.api_key = api_key
    transcript = aai.Transcriber().transcribe(audio_path)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(transcript.error)
    return TranscriptResult(
        provider="assemblyai",
        transcript=transcript.text or "",
        confidence=getattr(transcript, "confidence", None),
        raw=transcript.json_response,
    )
