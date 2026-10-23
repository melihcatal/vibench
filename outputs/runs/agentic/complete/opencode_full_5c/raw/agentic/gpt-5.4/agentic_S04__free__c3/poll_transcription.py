from __future__ import annotations

from typing import Any, Dict

from speech_client import AssemblyAIBatchSpeechClient


def poll_transcription(
    transcript_id: str, max_polls: int = 60, poll_interval_seconds: int = 5
) -> Dict[str, Any]:
    client = AssemblyAIBatchSpeechClient()
    job = client.wait_for_completion(
        transcript_id=transcript_id,
        max_polls=max_polls,
        poll_interval_seconds=poll_interval_seconds,
    )
    return {
        "provider": "AssemblyAI",
        "transcript_id": job.transcript_id,
        "status": job.status,
        "text": job.text,
        "confidence": job.confidence,
        "error": job.raw.get("error"),
    }
