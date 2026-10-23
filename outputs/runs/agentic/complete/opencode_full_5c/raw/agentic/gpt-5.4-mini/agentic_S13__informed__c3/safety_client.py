import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SafetyClientConfig:
    api_key: str
    project_id: Optional[str] = None
    endpoint: str = "https://api.perspectiveapi.com"


def load_safety_config() -> SafetyClientConfig:
    api_key = os.getenv("PERSPECTIVE_API_KEY", "")
    endpoint = os.getenv("PERSPECTIVE_API_ENDPOINT", "https://commentanalyzer.googleapis.com")
    return SafetyClientConfig(api_key=api_key, endpoint=endpoint)


def build_safety_headers(config: SafetyClientConfig) -> dict:
    return {"X-Goog-Api-Key": config.api_key, "Content-Type": "application/json"}
