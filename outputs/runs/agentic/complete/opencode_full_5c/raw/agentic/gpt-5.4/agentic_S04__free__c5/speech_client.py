from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


class AssemblyAIClient:
    def __init__(self, api_key: Optional[str] = None, timeout: int = 60) -> None:
        self.api_key = api_key or os.environ["ASSEMBLYAI_API_KEY"]
        self.timeout = timeout

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
        }

    def submit_transcript(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{ASSEMBLYAI_API_BASE}/transcript",
            json=payload,
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_transcript(self, transcript_id: str) -> Dict[str, Any]:
        response = requests.get(
            f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()


def require_openai_api_key() -> str:
    return os.environ["OPENAI_API_KEY"]


def maybe_target_language(value: Optional[str]) -> str:
    return value or os.environ.get("OPENAI_TRANSLATION_TARGET_LANGUAGE", "es")
