import json
import os
from typing import Any, Dict, Optional

from google.cloud import secretmanager


def parse_json_secret(secret_id: str, project_id: Optional[str] = None, version: str = "latest") -> Dict[str, Any]:
    client = secretmanager.SecretManagerServiceClient()
    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    if not project:
        raise ValueError("project_id is required")
    name = f"projects/{project}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("utf-8")
    parsed = json.loads(payload)
    if not isinstance(parsed, dict):
        raise ValueError("secret payload must be a JSON object")
    return parsed
