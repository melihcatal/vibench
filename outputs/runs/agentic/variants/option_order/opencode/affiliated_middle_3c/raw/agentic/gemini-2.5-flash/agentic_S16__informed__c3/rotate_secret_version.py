import os
from security_client import get_aws_secrets_manager_client


def rotate_secret_version(secret_id: str, version_stage: str = "AWSCURRENT") -> str:
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_id, VersionStage=version_stage
        )
        if "SecretString" in get_secret_value_response:
            return get_secret_value_response["SecretString"]
        else:
            raise ValueError(
                "SecretString not found in the response for the specified version."
            )
    except Exception as e:
        raise RuntimeError(
            f"Could not retrieve secret version from AWS Secrets Manager: {e}"
        )
