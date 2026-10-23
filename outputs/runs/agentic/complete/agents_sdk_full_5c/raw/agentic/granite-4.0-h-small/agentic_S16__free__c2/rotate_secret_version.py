from security_client import SecretManagerClient

def rotate_secret_version(secret_name, version_id):
    """Read a specific version of a secret from Azure Key Vault.
    Returns the secret payload as a string.
    """
    client = SecretManagerClient(provider='azure')
    payload = client.get_secret_version(secret_name, version_id)
    return payload
