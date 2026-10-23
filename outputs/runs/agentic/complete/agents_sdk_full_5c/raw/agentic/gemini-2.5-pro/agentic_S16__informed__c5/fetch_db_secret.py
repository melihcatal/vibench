"""Fetches a raw database connection secret from AWS Secrets Manager."""
import os
from typing import Optional

from security_client import get_secrets_manager_client


def fetch_db_secret_raw(secret_name: str) -> Optional[str]:
    """
    Fetches a raw secret string, typically JSON, from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret containing DB credentials.

    Returns:
        The raw secret string (often JSON), or None if an error occurs.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        # The secret is typically stored as a JSON string
        return get_secret_value_response.get('SecretString')
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Set AWS environment variables (region, credentials).
    db_secret_name = os.environ.get("DB_SECRET_NAME")
    if db_secret_name:
        raw_secret = fetch_db_secret_raw(db_secret_name)
        if raw_secret:
            print(f"Successfully fetched raw secret from: {db_secret_name}")
            print("Raw secret content:", raw_secret)
    else:
        print("Please set the DB_SECRET_NAME environment variable.")
