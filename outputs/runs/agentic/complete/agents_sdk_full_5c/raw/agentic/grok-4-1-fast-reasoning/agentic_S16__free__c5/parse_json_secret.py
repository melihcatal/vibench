from google.cloud import secretmanager
from typing import Dict, Any
from security_client import get_google_config
from security_models import parse_json_secret as parse_helper

def parse_json_secret(secret_id: str) -> Dict[str, Any]:
    config = get_google_config()
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    secret_str = response.payload.data.decode('UTF-8')
    return parse_helper(secret_str)
