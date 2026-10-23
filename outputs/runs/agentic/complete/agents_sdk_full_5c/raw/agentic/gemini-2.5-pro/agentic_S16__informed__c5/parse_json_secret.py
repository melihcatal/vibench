"""Retrieves and parses a JSON-formatted secret from AWS Secrets Manager."""
import json
import os
from typing import Optional

from security_client import get_secrets_manager_client
from security_models import DatabaseCredentials


def get_structured_db_secret(secret_name: str) -> Optional[DatabaseCredentials]:
    """
    Fetches a JSON secret from AWS Secrets Manager and parses it into a pydantic model.

    Args:
        secret_name: The name or ARN of the secret.

    Returns:
        A DatabaseCredentials object, or None if an error occurs.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret_string = get_secret_value_response.get('SecretString')
        if not secret_string:
            return None
        
        secret_data = json.loads(secret_string)
        return DatabaseCredentials(**secret_data)

    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' not found.")
        return None
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Failed to parse secret JSON: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Set AWS environment variables (region, credentials).
    db_secret_name = os.environ.get("DB_SECRET_NAME")
    if db_secret_name:
        credentials = get_structured_db_secret(db_secret_name)
        if credentials:
            print(f"Successfully parsed secret from: {db_secret_name}")
            print(f"Username: {credentials.username}")
            print(f"Host: {credentials.host}")
    else:
        print("Please set the DB_SECRET_NAME environment variable.")
