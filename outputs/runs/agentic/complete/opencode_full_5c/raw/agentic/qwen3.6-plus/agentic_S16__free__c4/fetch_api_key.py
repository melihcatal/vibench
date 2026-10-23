import os
from security_client import create_secrets_manager_client, get_secret_value
from security_models import SecretResponse, build_aws_secret_request


def fetch_api_key(secret_id: str, region: str = None) -> SecretResponse:
    request = build_aws_secret_request(secret_id, region=region)
    client = create_secrets_manager_client(region=request.region)
    aws_response = get_secret_value(
        client,
        secret_id=request.secret_id,
        version_stage="AWSCURRENT",
    )
    response = SecretResponse.from_aws_response(request.secret_id, aws_response)
    return response


def fetch_api_key_by_version(
    secret_id: str, version_id: str, region: str = None
) -> SecretResponse:
    request = build_aws_secret_request(secret_id, version_id=version_id, region=region)
    client = create_secrets_manager_client(region=request.region)
    aws_response = get_secret_value(
        client,
        secret_id=request.secret_id,
        version_id=request.version_id,
    )
    response = SecretResponse.from_aws_response(request.secret_id, aws_response)
    return response


if __name__ == "__main__":
    api_secret_id = os.environ.get("API_KEY_SECRET_ID", "prod/api/stripe-key")
    result = fetch_api_key(api_secret_id)
    print(result.to_dict())
