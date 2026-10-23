from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from google.cloud import secretmanager

from security_models import SecretPayload, normalize_secret_name, to_text_secret


@dataclass(frozen=True)
class SecretClientConfig:
    project_id: str

    @classmethod
    def from_env(cls) -> "SecretClientConfig":
        project_id = os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise RuntimeError("Missing GCP_PROJECT or GOOGLE_CLOUD_PROJECT")
        return cls(project_id=project_id)


@lru_cache(maxsize=1)
def get_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def secret_path(secret_id: str, version: str = "latest", project_id: Optional[str] = None) -> str:
    config = SecretClientConfig.from_env()
    project = project_id or config.project_id
    return f"projects/{project}/secrets/{normalize_secret_name(secret_id)}/versions/{version}"


def access_secret_text(secret_id: str, version: str = "latest", project_id: Optional[str] = None) -> SecretPayload:
    client = get_client()
    name = secret_path(secret_id, version=version, project_id=project_id)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    return to_text_secret(secret_id=secret_id, value=payload, version=version, provider="google-cloud-secret-manager")


def access_secret_bytes(secret_id: str, version: str = "latest", project_id: Optional[str] = None) -> bytes:
    client = get_client()
    name = secret_path(secret_id, version=version, project_id=project_id)
    response = client.access_secret_version(request={"name": name})
    return bytes(response.payload.data)


def access_secret_dict(secret_id: str, version: str = "latest", project_id: Optional[str] = None) -> Dict[str, Any]:
    payload = access_secret_text(secret_id=secret_id, version=version, project_id=project_id)
    return payload.as_json_dict()


def stage_secret_version(secret_id: str, payload: Dict[str, Any], project_id: Optional[str] = None) -> SecretPayload:
    client = get_client()
    config = SecretClientConfig.from_env()
    project = project_id or config.project_id
    parent = f"projects/{project}/secrets/{normalize_secret_name(secret_id)}"
    data = str(payload).encode("utf-8")
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": data}}
    )
    return SecretPayload(secret_id=secret_id, value=response.name, version=response.name.rsplit("/", 1)[-1], provider="google-cloud-secret-manager")
