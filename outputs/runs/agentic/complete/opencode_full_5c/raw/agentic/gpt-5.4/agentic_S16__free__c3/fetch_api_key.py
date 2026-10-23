from __future__ import annotations

from security_client import (
    build_secret_manager_client,
    build_secret_version_name,
    get_project_id,
)
from security_models import decode_secret_bytes


def fetch_api_key(
    secret_id: str, project_id: str | None = None, version_id: str = "latest"
) -> str:
    client = build_secret_manager_client()
    resource_name = build_secret_version_name(
        get_project_id(project_id), secret_id, version_id
    )
    response = client.access_secret_version(request={"name": resource_name})
    return decode_secret_bytes(response.payload.data)
