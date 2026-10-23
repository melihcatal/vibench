from __future__ import annotations

from typing import Any, Dict

from security_client import build_secret_reference, get_secret_manager_client
from security_models import parse_json_secret_value



def parse_json_secret(secret_id: str, version: str = "latest") -> Dict[str, Any]:
    client = get_secret_manager_client()
    ref = build_secret_reference(secret_id=secret_id, version=version)
    response = client.access_secret_version(request={"name": ref.resource_name()})
    secret_value = response.payload.data.decode("utf-8")
    parsed = parse_json_secret_value(secret_value)
    parsed["_gcp_secret_version"] = ref.version
    parsed["_provider"] = "Google Cloud Secret Manager"
    return parsed
