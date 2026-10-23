import os
from security_client import fetch_secret, get_secrets_manager_client
from security_models import SecretRequest, SecretResponse


def fetch_api_key(
    secret_id: str = None, version_stage: str = "AWSCURRENT"
) -> SecretResponse:
    target_id = secret_id or os.environ.get("API_KEY_SECRET_ID", "prod/api/primary-key")
    request = SecretRequest(
        secret_id=target_id,
        version_stage=version_stage,
        with_decryption=True,
    )
    return fetch_secret(request)


def fetch_api_key_raw(secret_id: str = None) -> str:
    response = fetch_api_key(secret_id)
    value = response.secret_value
    if isinstance(value, dict):
        return value.get("api_key", value.get("key", str(value)))
    return str(value)


if __name__ == "__main__":
    result = fetch_api_key()
    print(f"Secret ID: {result.secret_id}")
    print(f"Version: {result.version_id}")
    print(f"Stages: {result.version_stages}")
