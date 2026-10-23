from __future__ import annotations

from typing import Any, Dict

from speech_client import AssemblyAIClient
from speech_models import normalize_transcript_response


def poll_transcription(transcript_id: str) -> Dict[str, Any]:
    client = AssemblyAIClient()
    payload = client.get_transcript(transcript_id)
    transcript = normalize_transcript_response(payload)
    if transcript.status == "error":
        raise RuntimeError(transcript.error or "AssemblyAI transcription failed")
    return {
        "id": transcript.id,
        "status": transcript.status,
        "text": transcript.text,
        "provider": "assemblyai",
    }
