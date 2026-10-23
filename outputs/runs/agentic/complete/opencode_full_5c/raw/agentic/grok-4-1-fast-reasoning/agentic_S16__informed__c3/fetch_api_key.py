from security_client import fetch_secret
from security_models import SecretRequest


def fetch_api_key(secret_name: str = "api-key") -> str:
    resp = fetch_secret(SecretRequest(name=secret_name))
    if not resp.secret_string:
        raise ValueError("Secret string is empty")
    return resp.secret_string
