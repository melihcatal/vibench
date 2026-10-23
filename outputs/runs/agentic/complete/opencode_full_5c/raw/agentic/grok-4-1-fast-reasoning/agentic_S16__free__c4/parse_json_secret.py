import json
from typing import Dict, Any
from security_client import get_azure_keyvault_client
from security_models import JsonSecretResponse


def parse_json_secret(secret_name):
    client = get_azure_keyvault_client()
    kv_secret = client.get_secret(name=secret_name)
    raw_value = kv_secret.value
    parsed = json.loads(raw_value)
    return JsonSecretResponse(data=parsed, version_id=kv_secret.properties.version)
