from __future__ import annotations

import time
from typing import Any, Dict, Optional

from speech_client import get_transcript
from speech_models import TranscriptStatus


def poll_transcription(
    transcript_id: str,
    api_key: Optional[str] = None,
    timeout_seconds: int = 900,
    poll_interval_seconds: int = 5,
) -> Dict[str, Any]:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        payload = get_transcript(transcript_id, api_key=api_key)
        status = TranscriptStatus.from_assemblyai(payload)
        if status.status == "completed":
            return {
                "provider": "AssemblyAI",
                "transcript_id": status.transcript_id,
                "status": status.status,
                "text": status.text,
            }
        if status.status == "error":
            raise RuntimeError(status.error or "AssemblyAI transcription failed")
        time.sleep(poll_interval_seconds)
    raise TimeoutError(f"Timed out waiting for AssemblyAI transcript {transcript_id}")
