from __future__ import annotations

import json
import os
from typing import Optional

from google.cloud import secretmanager

from security_client import get_gcp_project_id, get_secret_version_name, secret_manager_client
from security_models import SecretFetchRequest, SecretFetchResponse, normalize_secret_payload


def fetch_db_secret(secret_id: str, version: str = "latest", project_id: Optional[str] = None) -> SecretFetchResponse:
    request = SecretFetchRequest(secret_id=secret_id, version=version, project_id=project_id or get_gcp_project_id())
    client = secret_manager_client()
    name = get_secret_version_name(request.project_id, request.secret_id, request.version)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    normalized = normalize_secret_payload(payload)
    if isinstance(normalized, dict):
        value = normalized
    else:
        try:
            value = json.loads(normalized)
        except Exception:
            value = {"connection_string": normalized}
    return SecretFetchResponse(
        secret_id=request.secret_id,
        version=request.version,
        project_id=request.project_id,
        value=value,
        provider="google-cloud-secret-manager",
    )


if __name__ == "__main__":
    secret_id = os.environ.get("GCP_DB_SECRET_ID", "db-connection")
    result = fetch_db_secret(secret_id)
    print(result.value)
