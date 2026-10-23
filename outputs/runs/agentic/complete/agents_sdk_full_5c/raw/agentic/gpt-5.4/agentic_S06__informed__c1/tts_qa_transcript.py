from __future__ import annotations

import os

import assemblyai as aai

from speech_models import TranscriptResult


ASSEMBLYAI_SPEECH_MODEL = "best"


def transcribe_qa_sample(audio_source: str) -> TranscriptResult:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise EnvironmentError("ASSEMBLYAI_API_KEY is required for AssemblyAI Transcripts API.")
    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(speech_model=ASSEMBLYAI_SPEECH_MODEL)
    transcript = aai.Transcriber(config=config).transcribe(audio_source)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(transcript.error)
    return TranscriptResult(
        transcript=transcript.text or "",
        confidence=getattr(transcript, "confidence", None),
        provider="assemblyai",
    )
