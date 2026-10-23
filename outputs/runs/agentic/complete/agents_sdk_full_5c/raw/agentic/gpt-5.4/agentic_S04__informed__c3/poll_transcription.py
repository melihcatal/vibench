from __future__ import annotations

from speech_client import AssemblyAIClient, ensure_completed


def poll_transcription(transcript_id: str) -> dict:
    client = AssemblyAIClient()
    result = client.get_transcription(transcript_id)
    if result.status == "completed":
        completed = ensure_completed(result)
        return {
            "provider": "AssemblyAI",
            "transcript_id": completed.transcript_id,
            "status": completed.status,
            "text": completed.text,
            "confidence": completed.confidence,
            "language_code": completed.language_code,
        }
    if result.status == "error":
        raise RuntimeError(result.raw.get("error") or "AssemblyAI transcription failed")
    return {
        "provider": "AssemblyAI",
        "transcript_id": result.transcript_id,
        "status": result.status,
    }
