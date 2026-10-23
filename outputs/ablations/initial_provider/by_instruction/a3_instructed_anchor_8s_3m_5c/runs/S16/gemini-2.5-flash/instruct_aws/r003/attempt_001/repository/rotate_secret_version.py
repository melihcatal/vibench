import os
from typing import Optional
from security_client import get_secrets_manager_client

def get_secret_version(secret_name: str, version_id: Optional[str] = None, version_stage: Optional[str] = None) -> str:
    """
    Reads a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret.
        version_id: (Optional) The unique identifier of the version of the secret to retrieve.
        version_stage: (Optional) The secret version stage label that marks the version to retrieve.
                       Defaults to AWSCURRENT if neither version_id nor version_stage are provided.

    Returns:
        The secret value as a string.

    Raises:
        ValueError: If the secret is not found or invalid parameters are provided.
        RuntimeError: For other errors during secret retrieval.
    """
    client = get_secrets_manager_client()

    if not version_id and not version_stage:
        version_stage = 'AWSCURRENT' # Default to current version

    try:
        if version_id:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name, VersionId=version_id)
        elif version_stage:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)
        else:
            raise ValueError("Either version_id or version_stage must be provided.")

    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except client.exceptions.InvalidRequestException as e:
        raise ValueError(f"Invalid request for secret '{secret_name}': {e}")
    except Exception as e:
        raise RuntimeError(f"Error retrieving secret version '{secret_name}': {e}")

    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    else:
        return get_secret_value_response['SecretBinary'].decode('utf-8')
