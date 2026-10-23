import os
import json
from security_client import get_secrets_manager_client


def fetch_database_secret(secret_name: str) -> dict:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    It is assumed the secret is stored as a JSON string.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret_string = get_secret_value_response["SecretString"]
        return json.loads(secret_string)
    except Exception as e:
        print(f"Error fetching secret {secret_name}: {e}")
        return None


if __name__ == "__main__":
    db_secret_name = os.environ.get("DB_SECRET_NAME")
    if db_secret_name:
        db_secret = fetch_database_secret(db_secret_name)
        if db_secret:
            print(f"Successfully fetched database secret from: {db_secret_name}")
            # print(f"Username: {db_secret.get('username')}")
    else:
        print("Please set the DB_SECRET_NAME environment variable.")
