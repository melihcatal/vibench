import json
import os
from typing import Any, Dict, Optional

from google.cloud import secretmanager


def parse_json_secret(secret_name: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    client = secretmanager.SecretManagerServiceClient()
    project = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    name = secret_name or os.environ["JSON_SECRET_NAME"]
    resource = f"projects/{project}/secrets/{name}/versions/latest"
    response = client.access_secret_version(request={"name": resource})
    return json.loads(response.payload.data.decode("utf-8"))
