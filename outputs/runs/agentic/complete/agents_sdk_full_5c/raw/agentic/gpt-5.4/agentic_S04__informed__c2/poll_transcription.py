from __future__ import annotations

import time
from typing import Any, Dict, Optional

from speech_client import build_speech_client
from speech_models import TranscriptStatus


def poll_transcription(transcript_id: str, timeout_seconds: int = 900, poll_interval_seconds: int = 5) -> Dict[str, Any]:
    client = build_speech_client()
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        raw = client.get_transcript(transcript_id)
        status = TranscriptStatus.from_assemblyai(raw)
        if status.status == "completed":
            return {
                "provider": "AssemblyAI",
                "transcript_id": status.id,
                "status": status.status,
                "text": status.text,
                "confidence": status.confidence,
            }
        if status.status == "error":
            raise RuntimeError(status.error or "AssemblyAI transcription failed")
        time.sleep(poll_interval_seconds)

    raise TimeoutError(f"Timed out waiting for AssemblyAI transcript {transcript_id}")
