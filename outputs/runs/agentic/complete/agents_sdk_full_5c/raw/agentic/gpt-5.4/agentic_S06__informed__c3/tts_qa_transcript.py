from __future__ import annotations

import os
from typing import Union

import assemblyai as aai

from speech_models import TranscriptResult


AudioInput = Union[str, bytes]


def transcribe_qa_sample(audio: AudioInput) -> TranscriptResult:
    aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(transcript.error)
    return TranscriptResult(
        provider="assemblyai",
        transcript=transcript.text or "",
        confidence=getattr(transcript, "confidence", None),
        raw=transcript.json_response,
    )
