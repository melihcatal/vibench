from security_client import SecretsManagerClient

def fetch_api_key(secret_name: str, region_name: str = 'us-east-1') -> str | None:
    client = SecretsManagerClient(region_name=region_name)
    secret = client.get_secret_value(secret_name)
    if secret:
        return secret.get_string_value()
    return None
