from __future__ import annotations

import os

import assemblyai as aai

from speech_models import TranscriptResult


def transcribe_qa_sample(audio_path: str) -> TranscriptResult:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing required environment variable: ASSEMBLYAI_API_KEY")
    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
    transcript = aai.Transcriber(config=config).transcribe(audio_path)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(transcript.error or "AssemblyAI transcription failed")
    return TranscriptResult(
        transcript=transcript.text or "",
        confidence=getattr(transcript, "confidence", None),
    )
