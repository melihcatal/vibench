import os
from pathlib import Path
from speech_client import get_openai_client
from speech_models import TranscriptResult


def transcribe_qa_sample(
    audio_path: str | Path,
    model: str = "whisper-1",
    language: str | None = None,
    response_format: str = "verbose_json",
) -> TranscriptResult:
    client = get_openai_client()
    path = Path(audio_path)
    with open(path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format=response_format,
            language=language,
        )
    text = response.text
    detected_language = language or response.language
    confidence = 1.0
    segments = []
    if hasattr(response, "segments") and response.segments:
        segments = [
            {
                "id": seg.id,
                "start": seg.start,
                "end": seg.end,
                "text": seg.text,
            }
            for seg in response.segments
        ]
        if segments and hasattr(response.segments[0], "avg_logprob"):
            import math

            avg_logprob = sum(
                getattr(seg, "avg_logprob", 0) for seg in response.segments
            ) / len(response.segments)
            confidence = min(1.0, max(0.0, math.exp(avg_logprob)))

    return TranscriptResult(
        text=text,
        language=detected_language,
        confidence=confidence,
        segments=segments,
    )
