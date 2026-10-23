import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class SecurityClientConfig:
    project_id: str
    provider: str = "google-cloud-secret-manager"
    api_version: str = "v1"
    location: str = "global"


def load_security_config() -> SecurityClientConfig:
    project_id = (
        os.environ.get("GCP_PROJECT")
        or os.environ.get("GOOGLE_CLOUD_PROJECT")
        or "demo-project"
    )
    return SecurityClientConfig(project_id=project_id)


def secret_manager_base_url(config: SecurityClientConfig) -> str:
    return f"https://secretmanager.googleapis.com/{config.api_version}/projects/{config.project_id}/secrets"


def auth_headers() -> Dict[str, str]:
    token = os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN", "")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def request_json(
    method: str, url: str, payload: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    response = requests.request(
        method, url, headers=auth_headers(), json=payload, timeout=30
    )
    response.raise_for_status()
    if response.text:
        return response.json()
    return {}


def encode_payload(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


def decode_secret_payload(payload: Any) -> Any:
    if isinstance(payload, (dict, list)):
        return payload
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if not isinstance(payload, str):
        return payload
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return payload
