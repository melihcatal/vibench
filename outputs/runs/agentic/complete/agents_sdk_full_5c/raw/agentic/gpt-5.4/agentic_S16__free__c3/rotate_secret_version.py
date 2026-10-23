from __future__ import annotations

from typing import Any, Dict, Optional

from google.cloud import secretmanager

from security_client import build_secret_version_name, get_project_id, get_secret_manager_client


DEFAULT_ROTATION_SECRET = "rotating-service-credential"


def read_secret_version(secret_id: str = DEFAULT_ROTATION_SECRET, project_id: Optional[str] = None, version_id: str = "latest") -> Dict[str, Any]:
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    name = build_secret_version_name(secret_id=secret_id, project_id=project_id, version_id=version_id)
    version = client.get_secret_version(request={"name": name})
    access = client.access_secret_version(request={"name": name})
    return {
        "secret_version_name": version.name,
        "state": secretmanager.SecretVersion.State(version.state).name,
        "etag": version.etag,
        "create_time": str(version.create_time),
        "payload": access.payload.data.decode("UTF-8"),
        "provider": "Google Cloud Secret Manager",
    }


def read_staged_alias(secret_id: str = DEFAULT_ROTATION_SECRET, project_id: Optional[str] = None, alias: str = "latest") -> Dict[str, Any]:
    resolved_project = get_project_id(project_id)
    name = f"projects/{resolved_project}/secrets/{secret_id}/versions/{alias}"
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    access = client.access_secret_version(request={"name": name})
    return {
        "requested_alias": alias,
        "resolved_name": access.name,
        "payload": access.payload.data.decode("UTF-8"),
        "provider": "Google Cloud Secret Manager",
    }
