from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager

from security_client import get_gcp_project_id, get_secret_version_name, secret_manager_client
from security_models import SecretFetchRequest, SecretFetchResponse, normalize_secret_payload


def fetch_api_key(secret_id: str, version: str = "latest", project_id: Optional[str] = None) -> SecretFetchResponse:
    request = SecretFetchRequest(secret_id=secret_id, version=version, project_id=project_id or get_gcp_project_id())
    client = secret_manager_client()
    name = get_secret_version_name(request.project_id, request.secret_id, request.version)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    return SecretFetchResponse(
        secret_id=request.secret_id,
        version=request.version,
        project_id=request.project_id,
        value=normalize_secret_payload(payload),
        provider="google-cloud-secret-manager",
    )


if __name__ == "__main__":
    secret_id = os.environ.get("GCP_API_KEY_SECRET_ID", "api-key")
    result = fetch_api_key(secret_id)
    print(result.value)
