import os
import json
from security_client import get_secrets_manager_client


def fetch_database_secret(secret_id: str) -> dict:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    The secret is expected to be a JSON string.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_id)
        secret_string = response.get("SecretString")
        if secret_string:
            return json.loads(secret_string)
        return {}
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret with ID '{secret_id}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Failed to parse JSON from secret: {secret_id}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


if __name__ == "__main__":
    db_secret_id = os.environ.get("DB_SECRET_ID", "my-app/db-credentials")
    db_creds = fetch_database_secret(db_secret_id)
    if db_creds:
        print(f"Successfully fetched database secret from: {db_secret_id}")
        print(f"Username: {db_creds.get('username')}")
    else:
        print(f"Failed to fetch database secret from: {db_secret_id}")
