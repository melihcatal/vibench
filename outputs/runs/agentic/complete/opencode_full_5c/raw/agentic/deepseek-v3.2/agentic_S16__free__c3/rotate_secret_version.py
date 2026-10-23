import os
import boto3
from botocore.exceptions import ClientError


def rotate_secret_version(
    secret_name: str, version_stage: str = "AWSCURRENT", version_id: str = None
) -> dict:
    """
    Read a specific secret version or staged value from AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        if version_id:
            response = client.get_secret_value(
                SecretId=secret_name, VersionId=version_id
            )
        else:
            response = client.get_secret_value(
                SecretId=secret_name, VersionStage=version_stage
            )

        result = {
            "secret_name": secret_name,
            "secret_value": response.get("SecretString"),
            "version_id": response.get("VersionId"),
            "version_stages": response.get("VersionStages", []),
            "created_date": response.get("CreatedDate"),
            "arn": response.get("ARN"),
        }

        if version_stage == "AWSPENDING":
            result["is_pending"] = True
            result["rotation_status"] = "pending"
        elif version_stage == "AWSCURRENT":
            result["is_current"] = True
            result["rotation_status"] = "current"
        elif version_stage == "AWSPREVIOUS":
            result["is_previous"] = True
            result["rotation_status"] = "previous"

        return result

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        elif error_code == "InvalidRequestException":
            raise ValueError(f"Invalid request for secret {secret_name}") from e
        elif error_code == "InvalidParameterException":
            raise ValueError(f"Invalid parameter for secret {secret_name}") from e
        elif error_code == "DecryptionFailure":
            raise ValueError(f"Decryption failed for secret {secret_name}") from e
        else:
            raise RuntimeError(f"Error fetching secret version: {e}") from e
