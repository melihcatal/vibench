import json
import os
from security_client import get_secrets_manager_client
from security_models import SecretValue


def fetch_db_secret(secret_name: str) -> SecretValue:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret_string = response["SecretString"]
            # Database secrets are often stored as JSON with keys like username, password, host, etc.
            # We return the whole JSON string as the value for simplicity, or specific fields if parsed.
            return SecretValue(
                name=secret_name,
                value=secret_string,
                arn=response.get("ARN"),
                version_id=response.get("VersionId"),
                created_date=response.get("CreatedDate"),
            )
        else:
            raise NotImplementedError("Binary secrets are not handled in this example.")
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching DB secret: {e}")
