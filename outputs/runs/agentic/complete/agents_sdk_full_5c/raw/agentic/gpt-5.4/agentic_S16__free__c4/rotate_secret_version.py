from __future__ import annotations

from typing import Optional

from google.cloud.secretmanager_v1.types import SecretVersion

from security_client import access_secret_payload, get_secret_version_metadata


def read_secret_version(secret_id: str, version_id: str = "latest", project_id: Optional[str] = None) -> dict:
    version: SecretVersion = get_secret_version_metadata(secret_id=secret_id, version_id=version_id, project_id=project_id)
    payload = access_secret_payload(secret_id=secret_id, version_id=version_id, project_id=project_id)
    return {
        "name": version.name,
        "state": SecretVersion.State(version.state).name,
        "create_time": version.create_time.isoformat() if version.create_time else None,
        "etag": version.etag,
        "value": payload.text,
    }
