from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from google.cloud import secretmanager

from security_client import get_gcp_project_id, get_secret_version_name, secret_manager_client
from security_models import SecretFetchRequest, SecretFetchResponse, normalize_secret_payload


def parse_json_secret(secret_id: str, version: str = "latest", project_id: Optional[str] = None) -> SecretFetchResponse:
    request = SecretFetchRequest(secret_id=secret_id, version=version, project_id=project_id or get_gcp_project_id())
    client = secret_manager_client()
    name = get_secret_version_name(request.project_id, request.secret_id, request.version)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    normalized = normalize_secret_payload(payload)
    parsed: Dict[str, Any] = json.loads(normalized if isinstance(normalized, str) else json.dumps(normalized))
    return SecretFetchResponse(
        secret_id=request.secret_id,
        version=request.version,
        project_id=request.project_id,
        value=parsed,
        provider="google-cloud-secret-manager",
    )


if __name__ == "__main__":
    secret_id = os.environ.get("GCP_JSON_SECRET_ID", "json-secret")
    result = parse_json_secret(secret_id)
    print(result.value)
