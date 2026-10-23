# rotate_secret_version.py
# [SAME-SCENARIO]
# Reads a specific secret version or staged value (HashiCorp Vault)
import os
import hvac

from security_client import get_vault_client

client = get_vault_client()

def rotate_secret_version(secret_path: str, version: int = 1) -> dict:
    """Retrieve a specific version of a secret from Vault.",
    if version == 0:
        # Default latest version
        version = 'latest'
    return client.secrets.kv.v2.read_secret_version(path=secret_path, version=version)['data']['data']

if __name__ == '__main__':
    secret = rotate_secret_version('my-secret', version=2)
    print('Requested version:', secret)