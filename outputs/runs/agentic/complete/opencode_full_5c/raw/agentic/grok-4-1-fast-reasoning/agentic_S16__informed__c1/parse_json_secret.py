import json
import os
from typing import Dict, Any
from security_client import get_google_secret_client


def parse_json_secret(secret_name: str, project_id: str = None) -> Dict[str, Any]:
    client = get_google_secret_client(project_id)
    project = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    name = f"projects/{project}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    secret_value = response.payload.data.decode("UTF-8")
    return json.loads(secret_value)
