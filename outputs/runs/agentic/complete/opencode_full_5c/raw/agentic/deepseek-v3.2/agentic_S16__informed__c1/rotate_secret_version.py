import os
import boto3
from botocore.exceptions import ClientError


def rotate_secret_version(secret_name, version_stage="AWSCURRENT", version_id=None):
    """
    Read a specific secret version or staged value from AWS Secrets Manager.
    Can fetch by version stage (default: AWSCURRENT) or specific version ID.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        if version_id:
            # Fetch specific version by ID
            response = client.get_secret_value(
                SecretId=secret_name, VersionId=version_id
            )
        else:
            # Fetch by version stage
            response = client.get_secret_value(
                SecretId=secret_name, VersionStage=version_stage
            )

        if "SecretString" in response:
            secret = response["SecretString"]
            metadata = {
                "version_id": response.get("VersionId"),
                "version_stages": response.get("VersionStages", []),
                "created_date": response.get("CreatedDate"),
                "arn": response.get("ARN"),
            }
            return secret, metadata
        else:
            raise ValueError("Secret is not in string format")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise Exception(f"Secret {secret_name} not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise Exception(f"Invalid request for secret {secret_name}")
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise Exception(f"Invalid version parameter for secret {secret_name}")
        else:
            raise Exception(f"Error fetching secret version: {e}")
