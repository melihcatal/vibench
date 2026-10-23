from __future__ import annotations

from typing import Any, Dict, Optional

from google.cloud import secretmanager

from security_client import build_secret_version_name, get_secret_manager_client
from security_models import parse_json_payload


DEFAULT_JSON_SECRET = "application-config-json"


def parse_json_secret(secret_id: str = DEFAULT_JSON_SECRET, project_id: Optional[str] = None, version_id: str = "latest") -> Dict[str, Any]:
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    name = build_secret_version_name(secret_id=secret_id, project_id=project_id, version_id=version_id)
    response = client.access_secret_version(request={"name": name})
    raw_text = response.payload.data.decode("UTF-8")
    parsed = parse_json_payload(raw_text)
    parsed.setdefault("_source", name)
    parsed.setdefault("_provider", "Google Cloud Secret Manager")
    return parsed
