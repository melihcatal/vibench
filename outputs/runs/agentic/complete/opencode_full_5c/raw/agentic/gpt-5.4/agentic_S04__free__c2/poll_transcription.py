from __future__ import annotations

from speech_client import ensure_completed, fetch_transcription


def poll_transcription(transcript_id: str) -> dict[str, str]:
    result = fetch_transcription(transcript_id)
    if result.status == "completed":
        completed = ensure_completed(result)
        return {
            "id": completed.transcript_id,
            "status": completed.status,
            "transcript": completed.text,
        }
    if result.status == "error":
        raise RuntimeError(result.raw.get("error") or "AssemblyAI transcription failed")
    return {"id": result.transcript_id, "status": result.status, "transcript": ""}
