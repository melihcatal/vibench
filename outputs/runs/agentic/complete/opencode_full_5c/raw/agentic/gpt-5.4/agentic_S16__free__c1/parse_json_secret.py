from __future__ import annotations

import json

from security_client import (
    build_secret_resource,
    get_gcp_project_id,
    secret_manager_client,
)


def parse_json_secret(
    secret_id: str, project_id: str | None = None, version_id: str = "latest"
) -> dict:
    project = get_gcp_project_id(project_id)
    client = secret_manager_client()
    name = build_secret_resource(project, secret_id, version_id)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    parsed = json.loads(payload)
    return {
        "provider": "google-secret-manager",
        "name": response.name,
        "data": parsed,
    }
