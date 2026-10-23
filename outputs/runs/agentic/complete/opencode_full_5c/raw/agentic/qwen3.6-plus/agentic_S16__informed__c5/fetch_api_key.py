import os
from security_models import SecretRequest, SecretResponse, SecretType
from security_client import fetch_secret_response


def fetch_api_key(
    secret_id: str,
    version_id: str = None,
    version_stage: str = "AWSCURRENT",
    region: str = None,
) -> SecretResponse:
    request = SecretRequest(
        secret_id=secret_id,
        secret_type=SecretType.API_KEY,
        version_id=version_id,
        version_stage=version_stage,
        region=region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    )
    response = fetch_secret_response(request)
    return response


if __name__ == "__main__":
    secret_id = os.environ.get("API_KEY_SECRET_ID", "prod/api/stripe-key")
    result = fetch_api_key(secret_id)
    print(f"Retrieved API key for secret: {result.secret_id}")
    print(f"Version: {result.version_id}")
    print(f"Key length: {len(result.secret_value)}")
