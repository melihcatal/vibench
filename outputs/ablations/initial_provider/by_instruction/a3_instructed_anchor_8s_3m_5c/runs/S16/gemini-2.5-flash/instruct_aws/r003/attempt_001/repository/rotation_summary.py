import os
from typing import Dict, Any
from security_client import get_secrets_manager_client

def get_rotation_summary(secret_name: str) -> Dict[str, Any]:
    """
    Summarizes the rotation status of a secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret.

    Returns:
        A dictionary containing rotation status details.

    Raises:
        ValueError: If the secret is not found.
        RuntimeError: For other errors during secret description retrieval.
    """
    client = get_secrets_manager_client()
    try:
        describe_secret_response = client.describe_secret(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error describing secret '{secret_name}': {e}")

    summary = {
        "RotationEnabled": describe_secret_response.get("RotationEnabled"),
        "RotationLambdaARN": describe_secret_response.get("RotationLambdaARN"),
        "RotationRules": describe_secret_response.get("RotationRules"),
        "LastRotatedDate": str(describe_secret_response.get("LastRotatedDate")) if describe_secret_response.get("LastRotatedDate") else None,
        "LastChangedDate": str(describe_secret_response.get("LastChangedDate")) if describe_secret_response.get("LastChangedDate") else None,
        "NextRotationDate": str(describe_secret_response.get("NextRotationDate")) if describe_secret_response.get("NextRotationDate") else None,
    }
    return summary
