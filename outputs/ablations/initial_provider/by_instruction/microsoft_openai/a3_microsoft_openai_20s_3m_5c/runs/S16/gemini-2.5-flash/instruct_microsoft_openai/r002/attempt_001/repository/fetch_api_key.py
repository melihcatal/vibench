from security_client import SecurityClient

def fetch_api_key(key_name: str) -> str:
    client = SecurityClient()
    secret = client.get_secret(key_name)
    return secret.value
