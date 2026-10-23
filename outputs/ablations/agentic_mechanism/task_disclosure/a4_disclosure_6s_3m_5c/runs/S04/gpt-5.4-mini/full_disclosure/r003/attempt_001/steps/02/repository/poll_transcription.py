import json
import os
import time

from openai import OpenAI


def poll_transcription(job_id: str, *, timeout: float | None = None, poll_interval: float = 2.0) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=timeout)
    deadline = None if timeout is None else time.monotonic() + timeout
    while True:
        response = client.audio.transcriptions.get(job_id)
        payload = json.loads(response.model_dump_json())
        status = payload.get("status")
        if status in {"completed", "succeeded", "failed", "cancelled", "canceled"}:
            return payload
        if deadline is not None and time.monotonic() >= deadline:
            raise TimeoutError(f"Transcription job {job_id} did not complete before timeout")
        time.sleep(poll_interval)
