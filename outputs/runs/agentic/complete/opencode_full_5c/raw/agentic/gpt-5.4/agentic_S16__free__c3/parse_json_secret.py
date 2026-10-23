from __future__ import annotations

from typing import Any, Dict

from security_client import (
    build_secret_manager_client,
    build_secret_version_name,
    get_project_id,
)
from security_models import decode_secret_bytes, parse_json_secret_value


def parse_json_secret(
    secret_id: str, project_id: str | None = None, version_id: str = "latest"
) -> Dict[str, Any]:
    client = build_secret_manager_client()
    resource_name = build_secret_version_name(
        get_project_id(project_id), secret_id, version_id
    )
    response = client.access_secret_version(request={"name": resource_name})
    return parse_json_secret_value(decode_secret_bytes(response.payload.data))
