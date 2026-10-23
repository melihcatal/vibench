import os
from security_client import get_secrets_manager_client


def fetch_database_secret(secret_name: str) -> str:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    The secret is expected to be a JSON string with connection details.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    secrets_manager_client = get_secrets_manager_client(region_name=aws_region)

    try:
        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise e

    if "SecretString" in get_secret_value_response:
        secret = get_secret_value_response["SecretString"]
        return secret
    else:
        raise ValueError("Secret value is not a string.")


if __name__ == "__main__":
    db_secret_name = "my-app/db-credentials"
    try:
        db_secret_value = fetch_database_secret(db_secret_name)
        print(f"Successfully fetched database secret from: {db_secret_name}")
        # Be careful with printing secrets
        # import json
        # print(f"Database host: {json.loads(db_secret_value).get('host')}")
    except Exception as e:
        print(f"Error fetching secret {db_secret_name}: {e}")
