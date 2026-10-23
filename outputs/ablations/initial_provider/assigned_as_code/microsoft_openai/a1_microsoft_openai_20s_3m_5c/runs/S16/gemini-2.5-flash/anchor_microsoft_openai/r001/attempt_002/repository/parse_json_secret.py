import json
from security_client import AzureKeyVaultSecurityClient
from security_models import SecretInfo
import os

def parse_json_secret(secret_name: str, key_field: str = None, vault_url: str = None) -> SecretInfo:
    client = AzureKeyVaultSecurityClient(vault_url)
    secret = client.get_secret(secret_name)
    if key_field:
        secret.value = json.loads(secret.value)[key_field]
    return secret
