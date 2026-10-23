from __future__ import annotations

import json

from security_client import (
    DEFAULT_PROVIDER,
    build_secret_resource,
    get_gcp_project_id,
    parse_version_from_name,
    secret_manager_client,
)
from security_models import SecretValue, normalize_secret_text


def fetch_db_secret(
    secret_id: str, project_id: str | None = None, version_id: str = "latest"
) -> dict:
    resolved_project = get_gcp_project_id(project_id)
    client = secret_manager_client()
    resource_name = build_secret_resource(resolved_project, secret_id, version_id)
    response = client.access_secret_version(request={"name": resource_name})
    secret = SecretValue(
        provider=DEFAULT_PROVIDER,
        resource_name=response.name,
        value=normalize_secret_text(response.payload.data),
        version=parse_version_from_name(response.name),
    )
    return {
        "provider": secret.provider,
        "resource_name": secret.resource_name,
        "version": secret.version,
        "connection": json.loads(secret.value),
    }
