import os

from security_client import get_secrets_client, normalize_secret_response


def fetch_api_key(secret_id: str = None) -> str:
    client = get_secrets_client()
    secret_id = secret_id or os.getenv("AWS_SECRET_API_KEY_ID", "api/key")
    response = client.get_secret_value(SecretId=secret_id)
    secret = normalize_secret_response(response)
    value = secret.get("SecretString")
    return value if isinstance(value, str) else str(value)
