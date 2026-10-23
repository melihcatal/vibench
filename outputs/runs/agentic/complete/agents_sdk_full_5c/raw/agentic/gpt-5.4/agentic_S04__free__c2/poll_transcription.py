from __future__ import annotations

import time
from typing import Any, Dict, Optional

from speech_client import create_session, raise_for_assemblyai_error, transcript_endpoint
from speech_models import normalize_transcript_response


TERMINAL_STATES = {"completed", "error"}


def poll_transcription(
    transcript_id: str,
    interval_seconds: float = 3.0,
    timeout_seconds: float = 300.0,
) -> Dict[str, Any]:
    session = create_session()
    deadline = time.monotonic() + timeout_seconds

    while True:
        response = session.get(transcript_endpoint(transcript_id), timeout=60)
        raise_for_assemblyai_error(response)
        result = normalize_transcript_response(response.json())

        if result.status in TERMINAL_STATES:
            if result.status == "error":
                raise RuntimeError(result.raw.get("error", "AssemblyAI transcription failed"))
            return {
                "provider": "AssemblyAI",
                "transcript_id": result.transcript_id,
                "status": result.status,
                "text": result.text,
                "raw": result.raw,
            }

        if time.monotonic() >= deadline:
            raise TimeoutError(f"Timed out waiting for AssemblyAI transcript {transcript_id}")
        time.sleep(interval_seconds)
