import os
from typing import Dict, Any
from security_client import SecretManagerClient
from security_models import SecretPayload


def parse_json_secret(secret_id: str, project_id: str = None) -> Dict[str, Any]:
    client = SecretManagerClient(project_id=project_id)
    json_secret = client.access_secret_version(secret_id=secret_id)
    return json_secret.payload.json
