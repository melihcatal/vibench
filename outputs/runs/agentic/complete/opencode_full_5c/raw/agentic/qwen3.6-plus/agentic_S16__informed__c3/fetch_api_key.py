import os
from typing import Optional
import boto3
from botocore.config import Config

from security_models import SecretRequest, SecretResponse
from security_client import get_aws_session, build_client_config


def fetch_api_key(secret_name: Optional[str] = None) -> SecretResponse:
    secret_name = secret_name or os.environ.get("API_KEY_SECRET_NAME", "prod/api-key")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    session = get_aws_session()
    config = build_client_config(region)
    client = session.client("secretsmanager", config=config, region_name=region)

    request = SecretRequest(secret_id=secret_name, version_stage="AWSCURRENT")

    response = client.get_secret_value(
        SecretId=request.secret_id,
        VersionStage=request.version_stage,
    )

    api_key = response.get("SecretString", "")

    return SecretResponse(
        secret_id=request.secret_id,
        secret_value=api_key,
        version_id=response.get("VersionId", ""),
        version_stage=request.version_stage,
        arn=response.get("ARN", ""),
        provider="aws-secrets-manager",
    )


if __name__ == "__main__":
    result = fetch_api_key()
    print(result.model_dump())
