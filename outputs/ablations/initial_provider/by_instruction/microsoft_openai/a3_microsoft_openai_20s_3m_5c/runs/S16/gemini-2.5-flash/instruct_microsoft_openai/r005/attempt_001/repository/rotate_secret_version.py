import os
from security_client import get_hashicorp_vault_client
from security_models import Secret

def rotate_secret_version(path: str, mount_point: str = 'secret', version: int = None) -> Secret:
    vault_url = os.environ.get("VAULT_ADDR")
    vault_token = os.environ.get("VAULT_TOKEN")
    
    if not vault_url or not vault_token:
        raise ValueError("VAULT_ADDR or VAULT_TOKEN environment variables not set.")
        
    client = get_hashicorp_vault_client(vault_url, vault_token)
    
    if not client.is_authenticated():
        raise Exception("HashiCorp Vault client not authenticated.")

    read_options = {"mount_point": mount_point}
    if version is not None:
        read_options["version"] = version

    response = client.secrets.kv.v2.read_secret_version(path=path, **read_options)
    
    secret_data = response['data']['data']
    secret_value = secret_data.get('value') # Assuming the secret value is stored under the key 'value'
    
    return Secret(name=path, value=secret_value, version=str(response['data']['metadata']['version']))
