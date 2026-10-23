from __future__ import annotations

import time
from typing import Any, Dict

from speech_client import get_transcription
from speech_models import normalize_transcript


_TERMINAL_STATES = {"completed", "error"}


def poll_transcription(transcript_id: str, poll_interval_seconds: float = 3.0, timeout_seconds: float = 300.0) -> Dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last = None
    while time.monotonic() < deadline:
        raw = get_transcription(transcript_id)
        normalized = normalize_transcript(raw)
        last = normalized
        if normalized.status in _TERMINAL_STATES:
            if normalized.status == "error":
                raise RuntimeError(raw.get("error", "AssemblyAI transcription failed"))
            return {
                "provider": "AssemblyAI Transcripts API",
                "transcript_id": normalized.transcript_id,
                "status": normalized.status,
                "text": normalized.text,
                "confidence": normalized.confidence,
                "language_code": normalized.language_code,
                "segments": [segment.__dict__ for segment in normalized.segments],
                "raw": raw,
            }
        time.sleep(poll_interval_seconds)
    raise TimeoutError(f"Timed out waiting for AssemblyAI transcript {transcript_id}; last_status={getattr(last, 'status', 'unknown')}")
