import time
from openai import OpenAI

from speech_client import load_config, normalize_transcript


def poll_transcription(job_id: str, interval_seconds: int = 5, timeout_seconds: int = 600):
    config = load_config("openai")
    client = OpenAI(api_key=config.api_key)
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        job = client.audio.transcriptions.retrieve(job_id)
        payload = job.model_dump() if hasattr(job, "model_dump") else job
        status = payload.get("status")
        if status in {"succeeded", "completed", "done"}:
            return normalize_transcript(payload)
        if status in {"failed", "error", "cancelled"}:
            return payload
        time.sleep(interval_seconds)
    return {"status": "timeout", "job_id": job_id}
