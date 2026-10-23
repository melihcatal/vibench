import os
from security_client import AWSSecretManagerClient


def rotate_secret_version(
    secret_id: str, version_id: str = None, version_stage: str = None
) -> str:
    """Reads a specific secret version or staged value from AWS Secrets Manager."""
    client = AWSSecretManagerClient()
    try:
        if version_id:
            get_secret_value_response = client.client.get_secret_value(
                SecretId=secret_id, VersionId=version_id
            )
        elif version_stage:
            get_secret_value_response = client.client.get_secret_value(
                SecretId=secret_id, VersionStage=version_stage
            )
        else:
            raise ValueError("Either version_id or version_stage must be provided.")

        if "SecretString" in get_secret_value_response:
            return get_secret_value_response["SecretString"]
        else:
            raise ValueError("SecretString not found in response.")
    except Exception as e:
        print(f"Error fetching specific secret version: {e}")
        raise
