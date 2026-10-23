from google.cloud import secretmanager
import json
from typing import Dict, Any
from security_client import get_provider_config
from security_models import JsonSecret, SecretMetadata


def parse_json_secret(secret_name: str) -> JsonSecret:
    config = get_provider_config("google")
    project_id = config["project_id"]
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    secret_value = response.payload.data.decode("UTF-8")
    metadata: SecretMetadata = {
        "name": secret_name,
        "version_id": response.name.split("/")[-1],
        "created_time": response.create_time.isoformat()
        if response.create_time
        else None,
    }
    parsed: Dict[str, Any] = json.loads(secret_value)
    return {"metadata": metadata, "parsed": parsed}
