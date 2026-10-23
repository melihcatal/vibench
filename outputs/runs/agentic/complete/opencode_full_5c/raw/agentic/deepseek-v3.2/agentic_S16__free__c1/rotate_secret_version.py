import os
import boto3
from botocore.exceptions import ClientError


def rotate_secret_version(
    secret_name: str, version_stage: str = "AWSCURRENT", version_id: str = None
):
    """
    Read a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager
        version_stage: Stage identifier (e.g., AWSCURRENT, AWSPENDING, AWSPREVIOUS)
        version_id: Specific version ID to retrieve (optional)

    Returns:
        Tuple of (secret_value, version_info)
    """
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        # Prepare request parameters
        request_params = {"SecretId": secret_name}

        if version_id:
            request_params["VersionId"] = version_id
        elif version_stage:
            request_params["VersionStage"] = version_stage

        response = client.get_secret_value(**request_params)

        # Extract secret value
        secret_value = response.get("SecretString")
        if not secret_value:
            # Handle binary secrets
            secret_value = response.get("SecretBinary")

        # Extract version information
        version_info = {
            "version_id": response.get("VersionId"),
            "version_stages": response.get("VersionStages", []),
            "created_date": response.get("CreatedDate"),
            "arn": response.get("ARN"),
            "name": response.get("Name"),
        }

        return secret_value, version_info

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        elif error_code == "InvalidRequestException":
            raise ValueError(f"Invalid request for secret {secret_name}") from e
        elif error_code == "InvalidParameterException":
            raise ValueError(f"Invalid parameter for secret {secret_name}") from e
        elif error_code == "DecryptionFailure":
            raise RuntimeError(f"Failed to decrypt secret {secret_name}") from e
        else:
            raise RuntimeError(f"Error retrieving secret {secret_name}: {e}") from e
