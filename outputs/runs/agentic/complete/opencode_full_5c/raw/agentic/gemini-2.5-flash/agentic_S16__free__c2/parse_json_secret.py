import os
import json
from typing import Any, Dict
from security_client import SecretManagerClient


def parse_json_secret(secret_id: str = "JSON_CONFIG") -> Dict[str, Any]:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable must be set.")

    client = SecretManagerClient(project_id=project_id)
    json_secret_data = client.access_secret(secret_id)

    return json.loads(json_secret_data)
