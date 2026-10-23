from __future__ import annotations

from typing import Any, Dict

from speech_client import assemblyai_get
from speech_models import normalize_assemblyai_transcript, transcript_text_from_segments


def poll_transcription(transcript_id: str) -> Dict[str, Any]:
    payload = assemblyai_get(f"/transcript/{transcript_id}")
    normalized = normalize_assemblyai_transcript(payload)
    text = normalized.text or transcript_text_from_segments(normalized.segments)
    return {
        "provider": "AssemblyAI",
        "transcript_id": normalized.transcript_id,
        "status": normalized.status,
        "transcript": text,
        "confidence": normalized.confidence,
        "language_code": normalized.language_code,
    }
