from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"
ASSEMBLYAI_API_KEY_ENV = "ASSEMBLYAI_API_KEY"


class AssemblyAIClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = ASSEMBLYAI_BASE_URL, timeout: int = 60):
        self.api_key = api_key or os.getenv(ASSEMBLYAI_API_KEY_ENV)
        if not self.api_key:
            raise ValueError(f"Missing API key in {ASSEMBLYAI_API_KEY_ENV}")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
        }

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/{path.lstrip('/')}",
            json=payload,
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/{path.lstrip('/')}",
            params=params,
            headers=self.headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()


def get_speech_client() -> AssemblyAIClient:
    return AssemblyAIClient()
