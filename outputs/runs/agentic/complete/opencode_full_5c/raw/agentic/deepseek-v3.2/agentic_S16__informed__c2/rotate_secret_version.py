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
        secret_name: Name of the secret in AWS Secrets Manager
        version_id: Specific version ID to retrieve (optional)
        version_stage: Version stage to retrieve (e.g., 'AWSCURRENT', 'AWSPENDING') (optional)

    Returns:
        The secret value for the specified version
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    kwargs = {"SecretId": secret_name}

    if version_id:
        kwargs["VersionId"] = version_id
    if version_stage:
        kwargs["VersionStage"] = version_stage

    try:
        response = client.get_secret_value(**kwargs)

        if "SecretString" in response:
            secret_value = response["SecretString"]
            retrieved_version_id = response.get("VersionId")
            version_stages = response.get("VersionStages", [])

            print(f"Retrieved secret '{secret_name}'")
            if retrieved_version_id:
                print(f"Version ID: {retrieved_version_id}")
            if version_stages:
                print(f"Version stages: {version_stages}")

            return secret_value
        else:
            raise ValueError("Secret is not in string format")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise ValueError(f"Invalid request for secret {secret_name}") from e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise ValueError(f"Invalid parameter for secret {secret_name}") from e
        elif e.response["Error"]["Code"] == "InvalidParameterValueException":
            raise ValueError(
                f"Invalid version specified for secret {secret_name}"
            ) from e
        else:
            raise RuntimeError(f"Error retrieving secret {secret_name}: {e}") from e
