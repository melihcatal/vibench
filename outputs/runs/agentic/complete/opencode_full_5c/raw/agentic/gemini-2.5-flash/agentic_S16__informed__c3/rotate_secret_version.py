import os
from security_client import get_aws_secrets_manager_client


def rotate_secret_version(secret_id: str, version_stage: str = "AWSCURRENT") -> str:
    """Reads a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_id: The ARN or name of the secret.
        version_stage: The secret version stage to retrieve. Defaults to "AWSCURRENT".
                       Common stages include AWSCURRENT, AWSPENDING, AWSPREVIOUS.

    Returns:
        The secret string for the specified version and stage.
    """
    client = get_aws_secrets_manager_client()
    try:
        response = client.get_secret_value(
            SecretId=secret_id, VersionStage=version_stage
        )
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_id}' not found.")
    except client.exceptions.InvalidRequestException as e:
        raise ValueError(
            f"Invalid request for secret '{secret_id}' with stage '{version_stage}': {e}"
        )
    except Exception as e:
        raise RuntimeError(
            f"Error fetching secret version '{secret_id}' with stage '{version_stage}': {e}"
        )

    if "SecretString" in response:
        return response["SecretString"]
    else:
        raise TypeError(
            f"Secret '{secret_id}' with stage '{version_stage}' did not contain a SecretString."
        )
