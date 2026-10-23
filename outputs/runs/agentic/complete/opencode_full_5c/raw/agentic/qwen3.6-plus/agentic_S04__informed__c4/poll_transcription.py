import time
from speech_client import get_transcription_status
from speech_models import (
    TranscriptionStatus,
    normalize_assemblyai_response,
    TranscriptionResult,
)


def poll_transcription(
    job_id: str, interval_seconds: int = 5, max_retries: int = 60
) -> TranscriptionResult:
    for attempt in range(max_retries):
        response = get_transcription_status(job_id)
        status = response.get("status", "")

        if status == "completed":
            return normalize_assemblyai_response(response)
        elif status == "error":
            raise RuntimeError(
                f"Transcription job {job_id} failed: {response.get('error')}"
            )

        time.sleep(interval_seconds)

    raise TimeoutError(
        f"Transcription job {job_id} did not complete within {max_retries * interval_seconds} seconds"
    )


if __name__ == "__main__":
    import os

    job_id = os.environ.get("TRANSCRIPTION_JOB_ID")
    if not job_id:
        raise ValueError("TRANSCRIPTION_JOB_ID environment variable is required")
    result = poll_transcription(job_id)
    print(f"Transcription complete: {result.text[:200]}...")
