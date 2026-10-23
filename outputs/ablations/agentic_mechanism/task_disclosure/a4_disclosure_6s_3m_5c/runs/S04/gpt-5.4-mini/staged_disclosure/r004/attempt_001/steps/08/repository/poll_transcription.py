import os
import time
from typing import Any, Dict, Optional

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


def poll_transcription(job_id: str, poll_interval: float = 2.0, timeout: Optional[float] = None) -> str:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")

    headers = {"authorization": api_key}
    start = time.monotonic()

    while True:
        response = requests.get(f"{ASSEMBLYAI_API_BASE}/transcript/{job_id}", headers=headers, timeout=30)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        status = data.get("status")

        if status == "completed":
            transcript = data.get("text")
            if not transcript:
                raise RuntimeError("Transcription completed but no transcript text was returned")
            return transcript

        if status == "error":
            raise RuntimeError(data.get("error", "Transcription failed"))

        if timeout is not None and (time.monotonic() - start) >= timeout:
            raise TimeoutError("Timed out waiting for transcription to complete")

        time.sleep(poll_interval)
