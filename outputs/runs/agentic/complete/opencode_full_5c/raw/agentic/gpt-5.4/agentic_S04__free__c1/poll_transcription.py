from __future__ import annotations

from typing import Any, Dict

from speech_client import AssemblyAIClient


def poll_transcription_job(
    transcript_id: str, max_attempts: int = 60, interval_seconds: float = 5.0
) -> Dict[str, Any]:
    client = AssemblyAIClient()
    result = client.poll_until_complete(
        transcript_id=transcript_id,
        max_attempts=max_attempts,
        interval_seconds=interval_seconds,
    )
    if result.status == "error":
        raise RuntimeError(result.raw.get("error", "AssemblyAI transcription failed"))
    return {
        "provider": "AssemblyAI",
        "transcript_id": result.transcript_id,
        "status": result.status,
        "text": result.text,
        "confidence": result.confidence,
        "language_code": result.language_code,
    }
