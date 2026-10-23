from __future__ import annotations

from typing import Any, Dict

from speech_client import AssemblyAISpeechClient
from speech_models import transcript_text


TERMINAL_STATES = {"completed", "error"}


def poll_transcription(transcript_id: str) -> Dict[str, Any]:
    client = AssemblyAISpeechClient()
    result = client.get_transcription(transcript_id)
    response: Dict[str, Any] = {
        "provider": "AssemblyAI",
        "id": result.get("id", transcript_id),
        "status": result.get("status"),
    }
    if result.get("status") == "completed":
        response["transcript"] = transcript_text(result)
    if result.get("status") == "error":
        response["error"] = result.get("error")
    return response
