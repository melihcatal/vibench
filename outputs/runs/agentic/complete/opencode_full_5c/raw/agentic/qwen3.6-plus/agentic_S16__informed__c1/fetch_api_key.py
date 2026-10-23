from security_client import build_secrets_manager_client
from security_models import (
    SecretRequest,
    SecretResponse,
    normalize_secret_response,
    build_secret_request,
)


def fetch_api_key(secret_id: str, version_stage: str = "AWSCURRENT") -> SecretResponse:
    client = build_secrets_manager_client()
    request = build_secret_request(secret_id, version_stage)

    params = {
        "SecretId": request.secret_id,
        "VersionStage": request.version_stage,
    }

    response = client.get_secret_value(**params)
    return normalize_secret_response(response)


if __name__ == "__main__":
    result = fetch_api_key("production/api-key")
    print(result.secret_value)
