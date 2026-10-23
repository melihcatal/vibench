import os
import hvac

vault_addr = os.getenv('VAULT_ADDR', 'https://vault.hashicorp.cloud')
vault_token = os.getenv('VAULT_TOKEN')
client = hvac.Client(url=vault_addr)
client.token = vault_token

def rotate_secret_version(secret_path: str, version: str = 'latest') -> dict:
    response = client.secrets.kv.v2.read_secret_version(path=secret_path, version=version)
    return response['data']['data']