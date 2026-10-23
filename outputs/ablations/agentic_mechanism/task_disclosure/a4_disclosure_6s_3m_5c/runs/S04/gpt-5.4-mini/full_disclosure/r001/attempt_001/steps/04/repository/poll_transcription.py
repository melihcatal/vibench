import os
from typing import Any, Dict, Optional

import requests


OPENAI_TRANSCRIPTION_BASE_URL = "https://api.openai.com/v1"


def poll_transcription(job_id: str, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.get(
        f"{OPENAI_TRANSCRIPTION_BASE_URL}/audio/transcriptions/{job_id}",
        headers={"Authorization": f"Bearer {key}"},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    if isinstance(data, dict) and data.get("status") in {"completed", "succeeded"}:
        return {"transcript": data.get("text") or data.get("transcript") or data}
    return data
