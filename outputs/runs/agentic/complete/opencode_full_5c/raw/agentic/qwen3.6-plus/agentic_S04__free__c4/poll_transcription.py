import time
from openai import OpenAI
from speech_client import get_openai_client
from speech_models import (
    TranscriptionJob,
    TranscriptionStatus,
    TranscriptionResult,
    normalize_transcription_response,
)


def poll_transcription(
    job_id: str, max_wait_seconds: int = 300, poll_interval: int = 5
) -> TranscriptionResult:
    client: OpenAI = get_openai_client()
    elapsed = 0
    while elapsed < max_wait_seconds:
        try:
            batch = client.batches.retrieve(job_id)
        except Exception:
            time.sleep(poll_interval)
            elapsed += poll_interval
            continue
        if batch.status == "completed":
            output_file = client.files.content(batch.output_file_id)
            import json

            results = json.loads(output_file.text)
            for result in results:
                if result.get("custom_id") == "transcription_001":
                    raw = result["response"]["body"]
                    return normalize_transcription_response(raw)
            return TranscriptionResult(job_id=job_id, text="", segments=[])
        elif batch.status in ("failed", "expired", "cancelled"):
            return TranscriptionResult(job_id=job_id, text="", segments=[])
        time.sleep(poll_interval)
        elapsed += poll_interval
    return TranscriptionResult(job_id=job_id, text="", segments=[])


def poll_job_status(job_id: str) -> TranscriptionJob:
    client: OpenAI = get_openai_client()
    batch = client.batches.retrieve(job_id)
    status_map = {
        "validating": TranscriptionStatus.QUEUED,
        "in_progress": TranscriptionStatus.PROCESSING,
        "finalizing": TranscriptionStatus.PROCESSING,
        "completed": TranscriptionStatus.COMPLETED,
        "failed": TranscriptionStatus.FAILED,
        "expired": TranscriptionStatus.FAILED,
        "cancelled": TranscriptionStatus.FAILED,
    }
    return TranscriptionJob(
        job_id=batch.id,
        status=status_map.get(batch.status, TranscriptionStatus.PROCESSING),
        error=batch.errors.model_dump() if batch.errors else None,
    )
