import os
import boto3
from security_client import get_aws_secrets_manager_client


def rotate_secret_version(secret_name: str, version_stage: str = "AWSCURRENT") -> str:
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name, VersionStage=version_stage
        )
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret {secret_name} not found.")
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(
            f"Secret version stage {version_stage} not found for secret {secret_name}."
        )
    except Exception as e:
        raise RuntimeError(
            f"Error fetching secret version {secret_name} with stage {version_stage}: {e}"
        )

    if "SecretString" in get_secret_value_response:
        return get_secret_value_response["SecretString"]
    else:
        raise ValueError(
            f"Secret {secret_name} version {version_stage} does not contain a SecretString."
        )
