from security_client import get_secrets_client


def fetch_api_key(secret_name: str) -> str:
    client = get_secrets_client()
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]
