import os
import time
from typing import Any, Dict, Optional

import requests


DEEPGRAM_API_BASE = "https://api.deepgram.com"


def poll_transcription(job_id: str, timeout: int = 300, interval: int = 5, api_key: Optional[str] = None) -> str:
    api_key = api_key or os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY is required")

    deadline = time.time() + timeout
    headers = {"Authorization": f"Token {api_key}"}
    url = f"{DEEPGRAM_API_BASE}/v1/listen/{job_id}"

    while True:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        payload: Dict[str, Any] = response.json()

        status = str(payload.get("status", "")).lower()
        if status in {"completed", "done", "success"}:
            results = payload.get("results", {})
            channels = results.get("channels", []) if isinstance(results, dict) else []
            if channels:
                alternatives = channels[0].get("alternatives", []) if isinstance(channels[0], dict) else []
                if alternatives:
                    transcript = alternatives[0].get("transcript", "")
                    if transcript:
                        return transcript
            if "transcript" in payload:
                return str(payload["transcript"])
            raise RuntimeError("Transcription completed but no transcript was found")

        if status in {"failed", "error"}:
            raise RuntimeError(f"Transcription job failed: {payload}")

        if time.time() >= deadline:
            raise TimeoutError("Timed out waiting for transcription job")

        time.sleep(interval)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: poll_transcription.py JOB_ID")

    print(poll_transcription(sys.argv[1]))
