from __future__ import annotations

from speech_client import AssemblyAISpeechClient


def poll_transcription(transcript_id: str) -> dict[str, object]:
    client = AssemblyAISpeechClient()
    result = client.get_transcription(transcript_id)
    return {
        "provider": "AssemblyAI",
        "transcript_id": result.transcript_id,
        "status": result.status,
        "text": result.text,
    }
