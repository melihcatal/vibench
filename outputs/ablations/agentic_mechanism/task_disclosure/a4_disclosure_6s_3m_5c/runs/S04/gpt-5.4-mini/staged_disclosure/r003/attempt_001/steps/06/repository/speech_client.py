import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


@dataclass(frozen=True)
class BatchSpeechConfig:
    api_key: str
    api_base: str = ASSEMBLYAI_API_BASE
    timeout_seconds: float = 30.0


def load_batch_speech_config(api_key: Optional[str] = None) -> BatchSpeechConfig:
    key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    return BatchSpeechConfig(api_key=key)


def _headers(api_key: str) -> Dict[str, str]:
    return {"authorization": api_key, "content-type": "application/json"}


class BatchSpeechClient:
    def __init__(self, config: Optional[BatchSpeechConfig] = None):
        self.config = config or load_batch_speech_config()

    def submit(self, audio_url: str, **options: Any) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"audio_url": audio_url}
        payload.update(options)
        response = requests.post(
            f"{self.config.api_base}/transcript",
            headers=_headers(self.config.api_key),
            json=payload,
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def get(self, transcript_id: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.config.api_base}/transcript/{transcript_id}",
            headers=_headers(self.config.api_key),
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, transcript_id: str, interval_seconds: float = 3.0, timeout_seconds: float = 600.0) -> Dict[str, Any]:
        import time

        start = time.time()
        while True:
            transcript = self.get(transcript_id)
            status = transcript.get("status")
            if status == "completed":
                return transcript
            if status == "error":
                raise RuntimeError(transcript.get("error", "transcription failed"))
            if time.time() - start > timeout_seconds:
                raise TimeoutError("timed out waiting for transcription")
            time.sleep(interval_seconds)
