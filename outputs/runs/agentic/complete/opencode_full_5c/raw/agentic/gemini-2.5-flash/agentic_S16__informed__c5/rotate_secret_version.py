import os
from typing import Optional
from security_client import get_secrets_manager_client
from security_models import Secret


def rotate_secret_version(
    secret_id: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> Optional[Secret]:
    """Reads a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_id: The name or ARN of the secret.
        version_id: The unique identifier of the version of the secret to retrieve.
        version_stage: The version stage of the secret to retrieve (e.g., 'AWSPENDING').

    Returns:
        A generic Secret object containing the secret value, or None if not found.
    """
    client = get_secrets_manager_client()
    try:
        params = {"SecretId": secret_id}
        if version_id:
            params["VersionId"] = version_id
        if version_stage:
            params["VersionStage"] = version_stage

        get_secret_value_response = client.get_secret_value(**params)

        secret_value = None
        if "SecretString" in get_secret_value_response:
            secret_value = get_secret_value_response["SecretString"]
        elif "SecretBinary" in get_secret_value_response:
            secret_value = get_secret_value_response["SecretBinary"]

        if secret_value is not None:
            return Secret(
                name=secret_id,
                value=secret_value,
                version_id=get_secret_value_response.get("VersionId"),
            )
        else:
            print(
                f"Secret '{secret_id}' did not contain a readable value for version/stage provided."
            )
            return None
    except client.exceptions.ResourceNotFoundException:
        print(
            f"Secret '{secret_id}' (version_id: {version_id}, version_stage: {version_stage}) not found."
        )
        return None
    except Exception as e:
        print(f"Error fetching secret '{secret_id}': {e}")
        return None
