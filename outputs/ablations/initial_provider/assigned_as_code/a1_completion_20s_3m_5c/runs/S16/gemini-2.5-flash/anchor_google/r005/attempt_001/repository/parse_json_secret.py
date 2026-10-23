import json
import os

from security_client import get_azure_key_vault_secret_client
from security_models import SecretPayload, SecretResponse

def parse_json_secret(payload: SecretPayload, vault_url: str) -> SecretResponse:
    client = get_azure_key_vault_secret_client(vault_url)
    
    # In Azure Key Vault, 'version' is part of the secret identifier
    # For simplicity, if a version is specified, we'll try to fetch that specific version.
    # Otherwise, we fetch the latest.
    if payload.version and payload.version != "latest":
        secret = client.get_secret(name=payload.secret_id, version=payload.version)
    else:
        secret = client.get_secret(name=payload.secret_id)
    
    json_value = secret.value
    
    if payload.key_field:
        json_value = json.loads(json_value)[payload.key_field]

    return SecretResponse(value=json_value, secret_id=payload.secret_id, version=secret.properties.version)
