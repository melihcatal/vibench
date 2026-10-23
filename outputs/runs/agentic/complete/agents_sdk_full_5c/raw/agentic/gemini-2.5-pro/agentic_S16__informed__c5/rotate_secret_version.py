"""Reads a specific secret version or staged value from AWS Secrets Manager."""
import os
from typing import Optional

from security_client import get_secrets_manager_client

def get_secret_by_stage(secret_name: str, stage: str) -> Optional[str]:
    """
    Fetches a specific version of a secret by its staging label.

    Common stages include 'AWSCURRENT', 'AWSPENDING', and 'AWSPREVIOUS'.

    Args:
        secret_name: The name or ARN of the secret.
        stage: The staging label of the version to retrieve.

    Returns:
        The secret string for the specified stage, or None on error.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=stage
        )
        return response.get('SecretString')
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' with stage '{stage}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Set AWS environment variables (region, credentials).
    secret_name_for_rotation = os.environ.get("ROTATING_SECRET_NAME")
    if secret_name_for_rotation:
        # Fetch the current version
        current_secret = get_secret_by_stage(secret_name_for_rotation, "AWSCURRENT")
        if current_secret:
            print(f"Successfully fetched 'AWSCURRENT' secret for {secret_name_for_rotation}")

        # Fetch the previous version, which may not exist
        previous_secret = get_secret_by_stage(secret_name_for_rotation, "AWSPREVIOUS")
        if previous_secret:
            print(f"Successfully fetched 'AWSPREVIOUS' secret for {secret_name_for_rotation}")
        else:
            print(f"No 'AWSPREVIOUS' version found for {secret_name_for_rotation}")

    else:
        print("Please set the ROTATING_SECRET_NAME environment variable.")
