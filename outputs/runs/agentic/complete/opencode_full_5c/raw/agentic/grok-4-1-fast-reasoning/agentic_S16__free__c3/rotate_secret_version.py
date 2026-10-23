import hvac
from typing import Dict, Optional
from security_client import get_vault_config
from security_models import SecretMetadata


def rotate_secret_version(secret_path: str, version: int = 1) -> SecretMetadata:
    vault_url, vault_token = get_vault_config()
    client = hvac.Client(url=vault_url)
    client.token = vault_token
    client.is_authenticated()
    response = client.secrets.kv.v2.read_secret_version(
        path=secret_path, version=version
    )
    data = response["data"]["data"]
    return {"value": data.get("secret_value", ""), "version": str(version)}
