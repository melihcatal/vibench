from __future__ import annotations

import os

import assemblyai as aai

from speech_models import TranscriptResult


def transcribe_qa_sample(audio_path: str) -> TranscriptResult:
    aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
    transcript = aai.Transcriber().transcribe(audio_path)
    if transcript.error:
        raise RuntimeError(transcript.error)
    return TranscriptResult(
        transcript=transcript.text or "",
        confidence=getattr(transcript, "confidence", None),
    )
