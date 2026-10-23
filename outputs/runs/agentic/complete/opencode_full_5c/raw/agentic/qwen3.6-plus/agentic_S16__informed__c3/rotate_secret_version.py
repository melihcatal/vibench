import os
from typing import Optional
import boto3
from botocore.config import Config

from security_models import SecretRequest, SecretResponse
from security_client import get_aws_session, build_client_config


def rotate_secret_version(
    secret_name: Optional[str] = None,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> SecretResponse:
    secret_name = secret_name or os.environ.get("ROTATION_SECRET_NAME", "prod/api-key")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    version_stage = version_stage or "AWSPENDING"
    version_id = version_id or os.environ.get("SECRET_VERSION_ID", "")

    session = get_aws_session()
    config = build_client_config(region)
    client = session.client("secretsmanager", config=config, region_name=region)

    request = SecretRequest(
        secret_id=secret_name,
        version_stage=version_stage,
        version_id=version_id if version_id else None,
    )

    kwargs: dict = {
        "SecretId": request.secret_id,
        "VersionStage": request.version_stage,
    }
    if request.version_id:
        kwargs["VersionId"] = request.version_id

    response = client.get_secret_value(**kwargs)

    secret_value = response.get("SecretString", "")

    return SecretResponse(
        secret_id=request.secret_id,
        secret_value=secret_value,
        version_id=response.get("VersionId", ""),
        version_stage=request.version_stage,
        arn=response.get("ARN", ""),
        provider="aws-secrets-manager",
    )


if __name__ == "__main__":
    result = rotate_secret_version()
    print(result.model_dump())
