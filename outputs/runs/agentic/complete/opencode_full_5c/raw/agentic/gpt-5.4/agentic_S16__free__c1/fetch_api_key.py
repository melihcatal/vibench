from __future__ import annotations

from security_client import (
    DEFAULT_PROVIDER,
    build_secret_resource,
    get_gcp_project_id,
    parse_version_from_name,
    secret_manager_client,
)
from security_models import SecretFetchRequest, SecretValue, normalize_secret_text


def fetch_api_key(
    secret_id: str, project_id: str | None = None, version_id: str = "latest"
) -> SecretValue:
    request = SecretFetchRequest(
        project_id=get_gcp_project_id(project_id),
        secret_id=secret_id,
        version_id=version_id,
    )
    client = secret_manager_client()
    resource_name = build_secret_resource(
        request.project_id, request.secret_id, request.version_id
    )
    response = client.access_secret_version(request={"name": resource_name})
    return SecretValue(
        provider=DEFAULT_PROVIDER,
        resource_name=response.name,
        value=normalize_secret_text(response.payload.data),
        version=parse_version_from_name(response.name),
    )
