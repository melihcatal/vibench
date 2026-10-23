import os
from google.cloud import secretmanager
from security_models import SecretConfig, parse_json_secret
from security_client import load_provider_env
from typing import Optional, Dict, Any

def retrieve_and_parse_json_secret(secret_name: Optional[str] = None) -> Dict[str, Any]:
    provider = 'google'
    load_provider_env(provider)
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'my-project')
    config = SecretConfig(name=secret_name or os.getenv('SECRET_NAME', 'json-secret'), project_id=project_id)
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config.project_id}/secrets/{config.name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    secret_value = response.payload.data.decode("UTF-8")
    return parse_json_secret(secret_value)