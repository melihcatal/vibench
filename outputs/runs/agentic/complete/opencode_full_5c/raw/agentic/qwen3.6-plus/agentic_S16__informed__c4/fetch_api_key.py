import os
from security_client import build_secret_request, fetch_secret
from security_models import SecretResponse


def fetch_api_key(secret_name: str, region: str = None) -> SecretResponse:
    api_key_name = secret_name or os.environ.get("API_KEY_SECRET_NAME", "prod/api-key")
    request = build_secret_request(
        secret_name=api_key_name,
        version_stage="AWSCURRENT",
        region=region,
    )
    return fetch_secret(request)


def get_api_key_value(secret_name: str = None, region: str = None) -> str:
    response = fetch_api_key(secret_name, region)
    return response.secret_value
