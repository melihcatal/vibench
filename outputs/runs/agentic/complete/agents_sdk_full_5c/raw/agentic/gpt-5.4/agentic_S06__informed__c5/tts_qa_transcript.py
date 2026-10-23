from __future__ import annotations

import os

import assemblyai as aai

from speech_models import TranscriptResult


ASSEMBLYAI_SPEECH_MODEL = "best"


def transcribe_qa_sample(audio_path: str) -> TranscriptResult:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("Missing ASSEMBLYAI_API_KEY")

    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(speech_model=ASSEMBLYAI_SPEECH_MODEL)
    transcript = aai.Transcriber(config=config).transcribe(audio_path)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(transcript.error)
    return TranscriptResult(
        provider="AssemblyAI",
        text=transcript.text or "",
        confidence=getattr(transcript, "confidence", None),
        utterances=[u.dict() if hasattr(u, "dict") else vars(u) for u in (transcript.utterances or [])],
        raw=transcript.json_response,
    )
