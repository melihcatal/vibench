from security_client import build_secrets_manager_client
from security_models import (
    SecretRequest,
    SecretResponse,
    normalize_secret_response,
    build_secret_request,
)


def rotate_secret_version(
    secret_id: str, version_id: str = None, version_stage: str = "AWSPENDING"
) -> SecretResponse:
    client = build_secrets_manager_client()
    request = build_secret_request(secret_id, version_stage)

    params = {
        "SecretId": request.secret_id,
        "VersionStage": request.version_stage,
    }

    if version_id:
        params["VersionId"] = version_id

    response = client.get_secret_value(**params)
    return normalize_secret_response(response)


if __name__ == "__main__":
    result = rotate_secret_version("production/api-key", version_stage="AWSPENDING")
    print(result.secret_value)
