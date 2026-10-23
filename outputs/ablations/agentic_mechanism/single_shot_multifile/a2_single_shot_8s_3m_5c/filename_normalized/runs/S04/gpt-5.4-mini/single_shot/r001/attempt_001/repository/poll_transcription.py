from typing import Optional

import requests

from speech_client import get_client_config, build_headers, build_url, raise_for_api_error
from speech_models import TranscriptionJob, TranscriptionResult


def poll_transcription(job_id: str, wait_seconds: float = 1.5, max_attempts: int = 60) -> TranscriptionResult:
    config = get_client_config()
    url = build_url(config, f"/v1/audio/transcriptions/{job_id}")
    headers = build_headers(config)
    last_job: Optional[TranscriptionJob] = None
    for _ in range(max_attempts):
        response = requests.get(url, headers=headers, timeout=config.timeout_seconds)
        if response.status_code >= 400:
            raise_for_api_error(response)
        last_job = TranscriptionJob.from_api(response.json())
        if last_job.is_finished:
            return last_job.to_result()
        if last_job.is_failed:
            raise RuntimeError(f"Transcription job failed: {last_job.status}")
        requests.utils.default_headers()
        import time
        time.sleep(wait_seconds)
    if last_job is None:
        raise RuntimeError("No transcription job state received")
    raise TimeoutError(f"Timed out waiting for transcription job {job_id}")
