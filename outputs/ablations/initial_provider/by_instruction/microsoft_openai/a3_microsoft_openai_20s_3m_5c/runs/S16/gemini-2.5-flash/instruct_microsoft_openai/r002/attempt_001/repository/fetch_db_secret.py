from security_client import SecurityClient

def fetch_db_secret(secret_name: str) -> str:
    client = SecurityClient()
    secret = client.get_secret(secret_name)
    return secret.value
