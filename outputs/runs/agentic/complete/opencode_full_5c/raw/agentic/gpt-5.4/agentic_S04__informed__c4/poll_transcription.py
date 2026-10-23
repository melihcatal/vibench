from __future__ import annotations

from speech_client import get_transcriber
from speech_models import normalize_assemblyai_transcript


def poll_transcription(transcript_id: str) -> dict:
    transcriber = get_transcriber()
    transcript = transcriber.get_by_id(transcript_id)
    result = normalize_assemblyai_transcript(transcript)
    return {
        "transcript_id": result.transcript_id,
        "status": result.status,
        "text": result.text,
        "confidence": result.confidence,
        "provider": "assemblyai",
    }
