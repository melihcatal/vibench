from __future__ import annotations

import time

from openai import OpenAI

from speech_client import get_client
from speech_models import extract_transcript_fields


def poll_transcription(job_id: str, timeout_s: int = 60, interval_s: float = 2.0) -> dict:
    client: OpenAI = get_client()
    deadline = time.time() + timeout_s
    last_payload = None
    while time.time() < deadline:
        last_payload = client.audio.transcriptions.retrieve(job_id)
        status = getattr(last_payload, "status", None) or last_payload.get("status")
        if status in {"completed", "succeeded", "done"}:
            result = extract_transcript_fields(last_payload)
            return {"status": status, "text": result.text, "segments": result.segments, "words": result.words, "raw": result.raw}
        if status in {"failed", "cancelled", "canceled"}:
            raise RuntimeError(f"transcription job {job_id} ended with status={status}")
        time.sleep(interval_s)
    raise TimeoutError(f"transcription job {job_id} did not complete in time; last_payload={last_payload}")
