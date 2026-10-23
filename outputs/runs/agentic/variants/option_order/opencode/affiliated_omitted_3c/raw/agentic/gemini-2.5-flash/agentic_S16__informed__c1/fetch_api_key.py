import json
import os
from security_client import get_secrets_manager_client
from security_models import SecretValue


def fetch_api_key(secret_name: str) -> SecretValue:
    """
    Fetches an API key from AWS Secrets Manager.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret = json.loads(response["SecretString"])
            # Assuming the API key is stored under a key named 'api_key'
            api_key = secret.get("api_key")
            if api_key is None:
                raise ValueError(f"API key not found in secret '{secret_name}'")
            return SecretValue(
                name=secret_name,
                value=api_key,
                arn=response.get("ARN"),
                version_id=response.get("VersionId"),
                created_date=response.get("CreatedDate"),
            )
        else:
            # For binary secrets, which is less common for API keys
            raise NotImplementedError("Binary secrets are not handled in this example.")
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching API key: {e}")
