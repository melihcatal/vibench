from __future__ import annotations

from typing import Optional

from google.cloud import secretmanager

from security_client import build_secret_reference, get_secret_manager_client
from security_models import SecretPayload, parse_version_id


def fetch_db_secret(secret_id: str, project_id: Optional[str] = None, version_id: str = "latest") -> SecretPayload:
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    ref = build_secret_reference(secret_id=secret_id, version_id=version_id, project_id=project_id)
    response = client.access_secret_version(request={"name": ref.resource_name})
    db_secret = response.payload.data.decode("utf-8")
    return SecretPayload(
        name=ref.resource_name,
        value=db_secret,
        version_id=parse_version_id(response.name),
        metadata={"provider": "Google Cloud Secret Manager", "runtime_fetch": True},
    )
