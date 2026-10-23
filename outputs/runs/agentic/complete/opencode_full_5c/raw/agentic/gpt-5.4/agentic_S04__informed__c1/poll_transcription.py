from __future__ import annotations

from typing import Any, Dict

from speech_client import build_transcriber
from speech_models import normalize_assemblyai_transcript


def poll_transcription(job_id: str) -> Dict[str, Any]:
    transcriber = build_transcriber()
    transcript = transcriber.get_by_id(job_id)
    normalized = normalize_assemblyai_transcript(transcript)
    return {
        "provider": "AssemblyAI",
        "job_id": normalized.job_id,
        "status": normalized.status,
        "transcript": normalized.text,
        "language_code": normalized.language_code,
        "confidence": normalized.confidence,
    }
