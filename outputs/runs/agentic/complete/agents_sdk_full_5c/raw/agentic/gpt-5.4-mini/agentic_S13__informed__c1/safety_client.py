import os
from dataclasses import dataclass
from typing import Optional

import requests

from safety_models import SafetyConfig, normalize_text


@dataclass
class SafetyServiceClient:
    endpoint: str
    api_key: str
    timeout: float = 30.0

    def post(self, path: str, payload: dict) -> dict:
        url = self.endpoint.rstrip("/") + path
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()


def load_config(prefix: str = "AZURE_CONTENT_SAFETY") -> SafetyConfig:
    return SafetyConfig(
        endpoint=os.environ.get(f"{prefix}_ENDPOINT", "").strip(),
        api_key=os.environ.get(f"{prefix}_KEY", "").strip(),
        project_id=os.environ.get("SAFETY_PROJECT_ID", "").strip() or None,
        threshold=float(os.environ.get("SAFETY_THRESHOLD", "0.5")),
    )


def build_client(config: Optional[SafetyConfig] = None) -> SafetyServiceClient:
    cfg = config or load_config()
    if not cfg.endpoint or not cfg.api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required")
    return SafetyServiceClient(endpoint=cfg.endpoint, api_key=cfg.api_key)


def clean_input(text: str) -> str:
    return normalize_text(text)
