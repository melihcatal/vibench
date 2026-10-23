import os
import boto3
from botocore.exceptions import ClientError


def rotate_secret_version(
    secret_name: str, version_stage: str = "AWSCURRENT", version_id: str = None
) -> dict:
    """
    Read a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager
        version_stage: The staging label of the version to retrieve (default: AWSCURRENT)
        version_id: Specific version ID to retrieve (optional, overrides version_stage)

    Returns:
        Dictionary containing secret value and metadata
    """
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        if version_id:
            # Get specific version by ID
            response = client.get_secret_value(
                SecretId=secret_name, VersionId=version_id
            )
        else:
            # Get version by staging label
            response = client.get_secret_value(
                SecretId=secret_name, VersionStage=version_stage
            )

        result = {
            "secret_name": secret_name,
            "arn": response.get("ARN"),
            "version_id": response.get("VersionId"),
            "version_stages": response.get("VersionStages", []),
            "created_date": response.get("CreatedDate"),
            "rotation_enabled": False,
        }

        # Get rotation info if available
        try:
            rotation_response = client.describe_secret(SecretId=secret_name)
            result["rotation_enabled"] = rotation_response.get("RotationEnabled", False)
            result["rotation_rules"] = rotation_response.get("RotationRules")
            result["last_rotated_date"] = rotation_response.get("LastRotatedDate")
            result["last_changed_date"] = rotation_response.get("LastChangedDate")
        except ClientError:
            # Secret may not have rotation configured
            pass

        if "SecretString" in response:
            result["secret_value"] = response["SecretString"]
            result["secret_type"] = "string"
        elif "SecretBinary" in response:
            result["secret_value"] = response["SecretBinary"]
            result["secret_type"] = "binary"
        else:
            raise ValueError("Secret has no value")

        return result

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        elif error_code == "InvalidRequestException":
            raise ValueError(f"Invalid request for secret {secret_name}") from e
        elif error_code == "InvalidParameterException":
            raise ValueError(f"Invalid parameter for secret {secret_name}") from e
        elif error_code == "AccessDeniedException":
            raise PermissionError(f"Access denied to secret {secret_name}") from e
        else:
            raise RuntimeError(f"Error fetching secret version: {e}") from e
