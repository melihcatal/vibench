from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager

from security_client import get_gcp_project_id, secret_manager_client
from security_models import SecretRotationRequest, SecretRotationResponse, normalize_secret_payload


def rotate_secret_version(secret_id: str, payload: str, version_alias: str = "latest", project_id: Optional[str] = None) -> SecretRotationResponse:
    request = SecretRotationRequest(secret_id=secret_id, payload=payload, version_alias=version_alias, project_id=project_id or get_gcp_project_id())
    client = secret_manager_client()
    parent = f"projects/{request.project_id}/secrets/{request.secret_id}"
    version = client.add_secret_version(
        request={"parent": parent, "payload": {"data": normalize_secret_payload(request.payload).encode("utf-8")}}
    )
    version_name = version.name
    if request.version_alias:
        client.update_secret(
            request={
                "secret": {"name": parent, "version_aliases": {request.version_alias: version_name.split("/")[-1]}},
                "update_mask": {"paths": ["version_aliases"]},
            }
        )
    return SecretRotationResponse(
        secret_id=request.secret_id,
        project_id=request.project_id,
        version_name=version_name,
        staged_value=request.payload,
        provider="google-cloud-secret-manager",
    )


if __name__ == "__main__":
    secret_id = os.environ.get("GCP_ROTATE_SECRET_ID", "rotate-secret")
    payload = os.environ.get("GCP_ROTATE_SECRET_PAYLOAD", "new-value")
    result = rotate_secret_version(secret_id, payload)
    print(result.version_name)
