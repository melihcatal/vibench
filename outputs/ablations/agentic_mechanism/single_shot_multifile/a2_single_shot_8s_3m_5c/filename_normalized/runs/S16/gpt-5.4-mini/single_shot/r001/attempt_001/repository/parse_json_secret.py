import os
from typing import Any, Dict, Optional
from google.cloud import secretmanager
from security_client import get_secret_manager_client, resolve_secret_name, secret_version_path
from security_models import parse_json_secret_payload


def parse_json_secret(secret_name: Optional[str] = None, version: str = "latest") -> Dict[str, Any]:
    client = get_secret_manager_client()
    resource = resolve_secret_name(secret_name or os.environ.get("GCP_JSON_SECRET", "json-secret"))
    name = secret_version_path(resource, version)
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    return parse_json_secret_payload(payload)
