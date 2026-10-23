import os
import time
from typing import Any, Dict, Optional

import requests

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def poll_transcription(job_id: str, api_key: Optional[str] = None, timeout_seconds: int = 300, interval_seconds: int = 5) -> Dict[str, Any]:
    token = api_key or os.environ.get("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")
    deadline = time.time() + timeout_seconds
    headers = {"Authorization": f"Bearer {token}"}
    last_response: Dict[str, Any] = {}
    while True:
        response = requests.get(f"{OPENAI_RESPONSES_URL}/{job_id}", headers=headers, timeout=30)
        response.raise_for_status()
        payload = response.json()
        last_response = payload
        status = payload.get("status") or payload.get("state")
        if status in {"completed", "succeeded", "done", "finished"}:
            transcript = payload.get("output_text") or payload.get("transcript") or payload.get("text") or payload
            return {"job_id": job_id, "status": status, "transcript": transcript, "response": payload}
        if status in {"failed", "cancelled", "canceled", "error"}:
            raise RuntimeError(f"transcription job {job_id} ended with status {status}")
        if time.time() >= deadline:
            raise TimeoutError(f"transcription job {job_id} did not complete within {timeout_seconds} seconds")
        time.sleep(interval_seconds)

