from __future__ import annotations

from typing import Any, Dict

from speech_client import build_transcriber, load_config
from speech_models import TranscriptionResponse, normalize_segments, normalize_transcript_text


def poll_transcription(job_id: str) -> TranscriptionResponse:
    cfg = load_config()
    transcriber = build_transcriber(cfg)
    transcript = transcriber.get_transcript(job_id)
    return TranscriptionResponse(
        job_id=job_id,
        status=getattr(transcript, "status", "completed"),
        transcript=normalize_transcript_text(getattr(transcript, "text", None)),
        segments=normalize_segments(transcript),
    )
