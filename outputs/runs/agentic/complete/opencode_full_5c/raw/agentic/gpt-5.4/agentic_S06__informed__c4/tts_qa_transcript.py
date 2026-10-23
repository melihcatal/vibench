from __future__ import annotations

import os
from pathlib import Path

import assemblyai as aai


def transcribe_qa_sample(audio_path: str | Path) -> dict:
    aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        str(audio_path),
        config=aai.TranscriptionConfig(speech_model=aai.SpeechModel.best),
    )
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(transcript.error)
    return {
        "provider": "AssemblyAI",
        "text": transcript.text or "",
        "confidence": getattr(transcript, "confidence", None),
        "id": transcript.id,
    }
