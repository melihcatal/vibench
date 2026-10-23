import os
from typing import Optional
from security_client import get_secrets_manager_client
from security_models import ApiKeySecret


def fetch_api_key(
    secret_name: str, version_stage: str = "AWSCURRENT"
) -> Optional[ApiKeySecret]:
    """Fetches an API key from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret to retrieve.
        version_stage: The version stage of the secret to retrieve (e.g., 'AWSCURRENT').

    Returns:
        An ApiKeySecret object containing the API key, or None if the secret is not found.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name, VersionStage=version_stage
        )
        if "SecretString" in get_secret_value_response:
            secret_value = get_secret_value_response["SecretString"]
            # Assuming the API key is stored as a plain string in the secret
            return ApiKeySecret(
                name=secret_name,
                key=secret_value,
                version_id=get_secret_value_response.get("VersionId"),
            )
        else:
            # Binary secret value, not expected for an API key in this scenario
            return None
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' not found.")
        return None
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        return None
