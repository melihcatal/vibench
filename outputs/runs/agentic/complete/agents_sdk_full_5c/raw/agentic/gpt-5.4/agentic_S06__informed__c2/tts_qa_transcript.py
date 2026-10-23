from __future__ import annotations

import assemblyai as aai

from speech_models import TranscriptResult


PROVIDER = "assemblyai"
SPEECH_MODEL = "best"


def transcribe_qa_sample(audio_path: str) -> TranscriptResult:
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speech_model=SPEECH_MODEL)
    transcript = transcriber.transcribe(audio_path, config=config)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(transcript.error)
    return TranscriptResult(
        transcript=transcript.text or "",
        confidence=getattr(transcript, "confidence", None),
        provider=PROVIDER,
        raw={"id": transcript.id, "status": str(transcript.status)},
    )
