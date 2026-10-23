import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SafetyClientConfig:
    endpoint: str
    key: str


def load_safety_config() -> SafetyClientConfig:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    return SafetyClientConfig(endpoint=endpoint, key=key)


def has_safety_credentials() -> bool:
    cfg = load_safety_config()
    return bool(cfg.endpoint and cfg.key)


def auth_headers() -> dict:
    cfg = load_safety_config()
    return {"Ocp-Apim-Subscription-Key": cfg.key, "Content-Type": "application/json"}


def endpoint_url(path: str) -> str:
    cfg = load_safety_config()
    return f"{cfg.endpoint}{path if path.startswith('/') else '/' + path}"
