import json
import os
from typing import Dict
from security_client import get_secret_manager_client, build_secret_name
from security_models import SecretPayload


def get_json_secret(project_id: str, secret_id: str) -> Dict:
    client = get_secret_manager_client()
    payload = SecretPayload(project_id=project_id, secret_id=secret_id)
    name = build_secret_name(payload)

    response = client.access_secret_version(request={"name": name})
    secret_string = response.payload.data.decode("UTF-8")
    return json.loads(secret_string)
