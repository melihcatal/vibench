from __future__ import annotations

from typing import Any, Dict, Optional

from google.cloud import secretmanager

from security_client import build_secret_reference, get_secret_manager_client
from security_models import parse_secret_json


def retrieve_json_secret(secret_id: str, project_id: Optional[str] = None, version_id: str = "latest") -> Dict[str, Any]:
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    ref = build_secret_reference(secret_id=secret_id, version_id=version_id, project_id=project_id)
    response = client.access_secret_version(request={"name": ref.resource_name})
    raw_secret = response.payload.data.decode("utf-8")
    parsed = parse_secret_json(raw_secret)
    parsed.setdefault("_provider", "google-cloud-secret-manager")
    parsed.setdefault("_secret_version", version_id)
    return parsed
