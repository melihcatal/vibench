import os
import time
from typing import Any, Dict, Optional

import requests


def poll_transcription(transcript_id: str, poll_interval_seconds: float = 5.0, timeout_seconds: Optional[float] = None) -> Dict[str, Any]:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")

    headers = {"authorization": api_key}
    url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    start = time.monotonic()

    while True:
        resp = requests.get(url, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")

        if status == "completed":
            return data
        if status == "error":
            raise RuntimeError(data.get("error", "Transcription failed"))

        if timeout_seconds is not None and (time.monotonic() - start) >= timeout_seconds:
            raise TimeoutError("Timed out while polling transcription job")

        time.sleep(poll_interval_seconds)
