from __future__ import annotations

import time
from typing import Any, Dict, Optional

from speech_client import ASSEMBLYAI_DEFAULT_POLL_SECONDS, get_assemblyai_transcript
from speech_models import normalize_assemblyai_transcript


_TERMINAL_FAILURES = {"error"}
_TERMINAL_SUCCESSES = {"completed"}


def poll_transcription(
    transcript_id: str,
    *,
    api_key: Optional[str] = None,
    poll_interval: float = ASSEMBLYAI_DEFAULT_POLL_SECONDS,
    timeout_seconds: float = 300,
) -> Dict[str, Any]:
    started = time.monotonic()
    while True:
        payload = get_assemblyai_transcript(transcript_id, api_key=api_key)
        job = normalize_assemblyai_transcript(payload)
        if job.status in _TERMINAL_SUCCESSES:
            return {
                "provider": "assemblyai",
                "job_id": job.job_id,
                "status": job.status,
                "transcript": job.text,
                "language_code": job.language_code,
                "raw": job.raw,
            }
        if job.status in _TERMINAL_FAILURES:
            raise RuntimeError(payload.get("error") or f"AssemblyAI transcript failed: {job.job_id}")
        if time.monotonic() - started >= timeout_seconds:
            raise TimeoutError(f"Timed out waiting for AssemblyAI transcript {transcript_id}")
        time.sleep(poll_interval)
