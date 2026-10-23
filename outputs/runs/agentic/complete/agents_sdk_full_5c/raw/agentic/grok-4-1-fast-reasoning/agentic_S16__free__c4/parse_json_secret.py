import json
from typing import Dict, Any

from security_client import get_azure_keyvault_client, get_env
from security_models import SecretResponse

def parse_json_secret(secret_id: str) -> Dict[str, Any]:
    client = get_azure_keyvault_client()
    secret_bundle = client.get_secret(secret_id)
    parsed = json.loads(secret_bundle.value)
    return {
        'name': secret_id,
        'value': secret_bundle.value,
        'version_id': secret_bundle.version,
        'parsed': parsed
    }