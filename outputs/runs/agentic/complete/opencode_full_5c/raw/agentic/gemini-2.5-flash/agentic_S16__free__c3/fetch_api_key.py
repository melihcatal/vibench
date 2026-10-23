import json
from security_client import get_secrets_manager_client
from security_models import SecretData


def fetch_api_key(secret_name: str) -> SecretData:
    """Fetches an API key from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to retrieve.

    Returns:
        A SecretData object containing the API key.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret_value = response["SecretString"]
        else:
            # Handle binary secrets if necessary, not covered in this example
            raise ValueError("Binary secret not supported in this example")

        return SecretData(
            name=secret_name,
            value=secret_value,
            arn=response.get("ARN"),
            version_id=response.get("VersionId"),
            created_date=response.get("CreatedDate"),
        )
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching API key: {e}")
