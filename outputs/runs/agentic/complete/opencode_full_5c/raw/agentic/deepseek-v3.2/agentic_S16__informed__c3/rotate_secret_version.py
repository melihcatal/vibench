import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional


def rotate_secret_version(
    secret_name: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> str:
    """
    Read a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret
        version_id: Specific version ID to retrieve (optional)
        version_stage: Version stage label like 'AWSCURRENT' or 'AWSPENDING' (optional)

    Returns:
        The secret value for the specified version
    """
    # AWS provider-specific client
    client = boto3.client(
        "secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    params = {"SecretId": secret_name}

    if version_id:
        params["VersionId"] = version_id
    if version_stage:
        params["VersionStage"] = version_stage

    try:
        response = client.get_secret_value(**params)

        # Return metadata about the version
        version_info = {
            "value": response.get("SecretString", ""),
            "version_id": response.get("VersionId", ""),
            "version_stages": response.get("VersionStages", []),
            "created_date": response.get("CreatedDate", "").isoformat()
            if response.get("CreatedDate")
            else "",
        }

        return version_info["value"]

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        elif error_code == "InvalidRequestException":
            raise ValueError(f"Invalid version request for secret {secret_name}") from e
        elif error_code == "InvalidParameterException":
            raise ValueError(
                f"Invalid version parameter for secret {secret_name}"
            ) from e
        else:
            raise RuntimeError(
                f"Error retrieving secret version {secret_name}: {e}"
            ) from e
