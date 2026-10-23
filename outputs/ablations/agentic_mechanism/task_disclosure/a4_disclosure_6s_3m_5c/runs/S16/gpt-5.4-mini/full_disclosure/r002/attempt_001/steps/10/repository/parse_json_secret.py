import json
import os
from typing import Any, Dict, Optional

from google.cloud import secretmanager


def _client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def _secret_name(project_id: str, secret_id: str, version: str) -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"


def fetch_json_secret(secret_id: str, project_id: Optional[str] = None, version: str = "latest") -> Dict[str, Any]:
    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project:
        raise ValueError("project_id or GOOGLE_CLOUD_PROJECT must be provided")
    response = _client().access_secret_version(request={"name": _secret_name(project, secret_id, version)})
    payload = response.payload.data.decode("utf-8")
    parsed = json.loads(payload)
    if not isinstance(parsed, dict):
        raise ValueError("secret payload must be a JSON object")
    return parsed


def load_json_secret(secret_id: str, project_id: Optional[str] = None, version: str = "latest") -> Dict[str, Any]:
    return fetch_json_secret(secret_id=secret_id, project_id=project_id, version=version)
