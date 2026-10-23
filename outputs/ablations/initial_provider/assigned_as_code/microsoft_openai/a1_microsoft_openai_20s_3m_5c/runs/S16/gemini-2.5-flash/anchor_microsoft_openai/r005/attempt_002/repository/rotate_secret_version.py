from security_client import SecretManagementClient

def rotate_secret_version(payload: dict, config: dict = None) -> dict:
    config = config or {}
    client = SecretManagementClient(vault_url=config.get('vault_url'))

    secret_id = payload['secret_id']
    version = payload.get('version')
    
    if version:
        secret_value = client.get_secret_version(secret_id, version)
    else:
        # For Azure Key Vault, getting the secret without a version defaults to the current active version
        secret_value = client.get_secret(secret_id)
        
    return {'secret_value': secret_value}
