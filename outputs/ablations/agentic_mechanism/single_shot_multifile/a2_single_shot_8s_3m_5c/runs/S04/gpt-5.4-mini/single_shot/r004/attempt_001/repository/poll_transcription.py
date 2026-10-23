from __future__ import annotations

from typing import Any, Dict

from speech_client import get_client
from speech_models import TranscriptionJob


def poll_transcription(job_id: str) -> Dict[str, Any]:
    client = get_client()
    job = client.transcriptions.get(job_id)
    if isinstance(job, TranscriptionJob):
        return job.to_dict()
    return job


if __name__ == '__main__':
    raise SystemExit(0)
