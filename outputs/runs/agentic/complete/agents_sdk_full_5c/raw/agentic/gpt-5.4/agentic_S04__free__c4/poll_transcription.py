from __future__ import annotations

from speech_client import assemblyai_get
from speech_models import normalize_assemblyai_transcript


TERMINAL_STATES = {"completed", "error"}


def poll_transcription(transcript_id: str) -> dict:
    response = assemblyai_get(f"/transcript/{transcript_id}")
    transcript = normalize_assemblyai_transcript(response)
    result = {
        "provider": "AssemblyAI",
        "transcript_id": transcript.transcript_id,
        "status": transcript.status,
    }
    if transcript.status == "completed":
        result["text"] = transcript.text
    if transcript.status == "error":
        result["error"] = transcript.error
    result["done"] = transcript.status in TERMINAL_STATES
    return result
