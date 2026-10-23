import boto3
import os
from botocore.exceptions import ClientError
from typing import Optional


def rotate_secret_version(
    secret_name: str, version_id: Optional[str] = None, stage: Optional[str] = None
) -> dict:
    """
    Read a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret
        version_id: Specific version ID to retrieve (optional)
        stage: Secret stage to retrieve ('AWSCURRENT', 'AWSPENDING', 'AWSPREVIOUS')

    Returns:
        Dictionary containing secret value and metadata
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        kwargs = {"SecretId": secret_name}

        if version_id:
            kwargs["VersionId"] = version_id
        if stage:
            kwargs["VersionStage"] = stage

        response = client.get_secret_value(**kwargs)

        result = {
            "secret_name": secret_name,
            "arn": response.get("ARN"),
            "created_date": response.get("CreatedDate"),
            "version_id": response.get("VersionId"),
            "version_stages": response.get("VersionStages", []),
            "secret_type": "string" if "SecretString" in response else "binary",
        }

        if "SecretString" in response:
            result["secret_value"] = response["SecretString"]
        elif "SecretBinary" in response:
            result["secret_value"] = response["SecretBinary"]

        return result

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise Exception(f"Secret '{secret_name}' not found")
        elif error_code == "InvalidRequestException":
            raise Exception(f"Invalid request for secret '{secret_name}': {e}")
        elif error_code == "InvalidParameterException":
            raise Exception(f"Invalid parameter for secret '{secret_name}': {e}")
        else:
            raise Exception(f"AWS Secrets Manager error: {e}")


def get_pending_secret(secret_name: str) -> dict:
    """
    Get the pending (staged) secret value for rotation.

    Args:
        secret_name: Name of the secret

    Returns:
        Pending secret value and metadata
    """
    return rotate_secret_version(secret_name, stage="AWSPENDING")


def get_current_secret(secret_name: str) -> dict:
    """
    Get the current active secret value.

    Args:
        secret_name: Name of the secret

    Returns:
        Current secret value and metadata
    """
    return rotate_secret_version(secret_name, stage="AWSCURRENT")


def get_previous_secret(secret_name: str) -> dict:
    """
    Get the previous secret value (before last rotation).

    Args:
        secret_name: Name of the secret

    Returns:
        Previous secret value and metadata
    """
    return rotate_secret_version(secret_name, stage="AWSPREVIOUS")


if __name__ == "__main__":
    current_secret = get_current_secret("prod/api-key")
    print(f"Current secret version: {current_secret['version_id']}")
    print(f"Secret stages: {current_secret['version_stages']}")

    try:
        pending_secret = get_pending_secret("prod/api-key")
        print(f"Pending secret exists: {pending_secret['version_id']}")
    except Exception as e:
        print(f"No pending secret: {e}")
