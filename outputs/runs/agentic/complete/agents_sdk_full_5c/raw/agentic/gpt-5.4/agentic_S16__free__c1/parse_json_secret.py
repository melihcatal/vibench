from __future__ import annotations

from typing import Any, Dict

from security_client import SecretManagementConfig, access_secret_version
from security_models import decode_secret_bytes, parse_json_secret_text



def parse_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> Dict[str, Any]:
    config = SecretManagementConfig(project_id=project_id, secret_id=secret_id, version_id=version_id)
    response = access_secret_version(config.resource_name)
    secret_text = decode_secret_bytes(response.payload.data)
    parsed = parse_json_secret_text(secret_text)
    parsed["_gcp_secret_version_name"] = response.name
    return parsed
